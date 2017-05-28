# -*- coding: utf-8 -*-
'''
程序功能：为数据文件(前30个部门）添加一列代表情感值的列
'''
import pandas
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from snownlp import SnowNLP
import datetime
import numpy

filenames=os.listdir('./ShenZhen_gov_info')
sizes=[os.path.getsize('./ShenZhen_gov_info/'+ filename) for filename in os.listdir('./ShenZhen_gov_info')]

fileWithSize=pandas.DataFrame({
        'filename':filenames,
        'size':sizes
   })

#得到 咨询内容前30的部门加上所有部门对应的文件名
first31files=fileWithSize.sort_values(by=['size'], ascending=False)[0:31]
                                     
names=['编号','标题','接收信箱','询问日期','回复日期','询问内容','回复内容']
flag=True
if not os.path.exists("附带情感值的文本数据"):
    os.mkdir("附带情感值的文本数据")
    
meanSentiments=[]
for filename in first31files.filename:
    if flag:
        df=pandas.read_csv('./ShenZhen_gov_info/'+ filename,encoding='GBK')
        flag=False
        continue
    else:
        df=pandas.read_csv('./ShenZhen_gov_info/'+ filename,names=names,encoding='GBK')
        
    #得到每一条提问内容的情感值
    sentiments=[]
    for askContent in df.询问内容:
        sentiments.append(SnowNLP(askContent).sentiments)
    
    df['情感值']=sentiments   
    df=df.sort_values(by=['情感值'],ascending=True)
    meanSentiments.append(numpy.mean(sentiments))
    filepath='附带情感值的文本数据/'+filename.split('.')[0]+'_附带情感值的数据.csv'
    df.to_csv(filepath,index=False,header=True)
    print('Sacve file: '+filepath)
     
#    date=[date[0:4] for date in df.询问日期]
#    #计算每年的咨询数目并根据数目大小排序
#    newdf=pandas.DataFrame({'date':date}).date.value_counts().sort_index()
    
    
#    newdate=[]
#    sumSentimentsOnOneYear=[]#单年的情感指数
#    #转换日期的格式从str为datetime.strptime，用于绘图
#    for date in newdf.index:
#        newdate.append(datetime.datetime.strptime(date, '%Y'))
#        sumSentimentsOnOneYear.append(df[df.询问日期==date].情感值.mean())
#    
#    dates=mdates.date2num(newdate)
#    fig, ax = plt.subplots()
#    #设置图片大小
#    #fig.set_size_inches(18.5, 10.5)
#    ax.set_xticks(dates) # Tickmark + label at every plotted point
#    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
#    
#    ax.plot_date(dates,sumSentimentsOnOneYear, ls='-', marker='o')
#    #ax.set_title('repost number')
#    ax.set_ylabel('情感值',fontproperties='SimHei',fontsize=15)
#    ax.set_xlabel('年份',fontproperties='SimHei',fontsize=15)
#    
#    # Format the x-axis for dates (label formatting, rotation)
#    fig.autofmt_xdate(rotation=45)
#    fig.tight_layout()
#        
#    #plt.show()
#    filepath='情感年度变化图/'+filename.split('.')[0]+'_情感年度变化图.png'
#    fig.savefig(filepath)
#    print('save file: '+filepath)

allList=pandas.DataFrame({
        '部门':first31files.filename[1:],
        '情感均值':meanSentiments
   })
allList=allList.sort_values(by=['情感均值'],ascending=True)
allList.to_csv('前30个部门的情感均值.csv',index=False,header=True)