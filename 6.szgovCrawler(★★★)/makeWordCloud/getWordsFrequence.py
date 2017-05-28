# -*- coding: utf-8 -*-
''''
程序功能：得到各个部门的询问内容的词频，并保存到csv文件中
'''
import jieba
import numpy
import pandas
import os

#filename='整合的所有信息'
#df=pandas.read_csv('../'+filename+'.csv',encoding='GBK')

filenames=os.listdir('../ShenZhen_gov_info')
sizes=[os.path.getsize('../ShenZhen_gov_info/'+ filename) for filename in os.listdir('../ShenZhen_gov_info')]

fileWithSize=pandas.DataFrame({
        'filename':filenames,
        'size':sizes
   })

if not os.path.exists("词频统计"):
    os.mkdir("词频统计")

data=[]
#得到 咨询内容前30的部门加上所有部门对应的文件名
first31files=fileWithSize.sort_values(by=['size'], ascending=False)[0:31]
                                     
names=['编号','标题','接收信箱','询问日期','回复日期','询问内容','回复内容']
cnt=1
flag=True
for filename in first31files.filename:
    if flag:
        df=pandas.read_csv('../ShenZhen_gov_info/'+ filename,encoding='GBK')
        flag=False
    else:
        df=pandas.read_csv('../ShenZhen_gov_info/'+ filename,names=names,encoding='GBK')
        
    contents=''
    for string in df.询问内容.values:
        contents += string
    #使用jieba进行分词，将分词结果存储在一个list中
    segments = []
    segs = jieba.cut(contents)
    for seg in segs:
        if len(seg)>1 and not seg.isdigit():#过滤一个字的词或者标点符号或数字
            segments.append(seg)
    
    #为方便统计词频，把结果保存在pandas的DataFrame中
    segmentDF = pandas.DataFrame({'词语':segments})
    
    #读取设定停用词的CSV文件(文件中只有一列数据)，移除停用词
    #注意：如果想对WeiBoStopwords这个文件添加新的停用词，不要用windows的记事本打开！！！！否则会报错
    stopwords = pandas.read_csv("Stopwords.txt",encoding='utf-8')
    
    #过滤segmentDF中为停用词的数据
    segmentDF = segmentDF[~segmentDF.词语.isin(stopwords.stopword)]
    
    #对词频进行统计,按照频率从高到低排列数据
    segStat = segmentDF.groupby(by=["词语"])["词语"].agg({"计数":numpy.size}).reset_index().sort_values(by=["计数"], ascending=False)
    
    data.append(segStat)
    
    filepath='词频统计/'+str(cnt)+'.'+filename.split('.')[0]+'_词频统计.csv'
    segStat.to_csv(filepath,mode='w',header=True,index=False)
    print("得到 <"+filename+"> 的词频统计信息")
    cnt=cnt+1
