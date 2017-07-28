# -*- coding: utf-8 -*-
''''
正常运行这份代码需要如下文件：
1.xxx.csv 欲进行分词的文件
2.simhei.ttf 绘制词云图时需要字体文件
3.Stopwords.txt 停用词文件
'''
import jieba
import numpy
import pandas
import os
from wordcloud import WordCloud

#filename='整合的所有信息'
#df=pandas.read_csv('../'+filename+'.csv',encoding='GBK')

filenames=os.listdir('../ShenZhen_gov_info')
sizes=[os.path.getsize('../ShenZhen_gov_info/'+ filename) for filename in os.listdir('../ShenZhen_gov_info')]

fileWithSize=pandas.DataFrame({
        'filename':filenames,
        'size':sizes
   })
if not os.path.exists("../词云图"):
    os.mkdir("../词云图")
#得到 咨询内容前30的部门加上所有部门对应的文件名
first31files=fileWithSize.sort_values(by=['size'], ascending=False)[0:31]
                                     
names=['编号','标题','接收信箱','询问日期','回复日期','询问内容','回复内容']
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
    segmentDF = pandas.DataFrame({'segment':segments})
    
    #读取设定停用词的CSV文件(文件中只有一列数据)，移除停用词
    #注意：如果想对WeiBoStopwords这个文件添加新的停用词，不要用windows的记事本打开！！！！否则会报错
    stopwords = pandas.read_csv("Stopwords.txt",encoding='utf-8')
    
    #过滤segmentDF中为停用词的数据
    segmentDF = segmentDF[~segmentDF.segment.isin(stopwords.stopword)]
    
    #对词频进行统计,按照频率从高到低排列数据
    segStat = segmentDF.groupby(by=["segment"])["segment"].agg({"计数":numpy.size}).reset_index().sort_values(by=["计数"], ascending=False)
    #设置词云对象参数
    wordcloud = WordCloud(font_path='simhei.ttf',background_color="black")
    
    #使用数据构建词云对象
    wordcloud = wordcloud.fit_words(segStat.head(1000).itertuples(index=False))
    """
    对于itertuples函数，可参考下面的测试：
    
    for i in segStat.head(5).itertuples(index=False):
        print(i)
    
    上述代码的输出结果为：
    Pandas(segment='\r\n', 计数=4923)
    Pandas(segment='政策', 计数=456)
    Pandas(segment='购房', 计数=417)
    Pandas(segment='合同', 计数=402)
    Pandas(segment='17', 计数=343)
    """
    filepath='../词云图/'+filename.split('.')[0]+'_wordcloud.jpg'
    wordcloud.to_file(filepath)
    print('save file :'+filepath)
#   plt.close()
