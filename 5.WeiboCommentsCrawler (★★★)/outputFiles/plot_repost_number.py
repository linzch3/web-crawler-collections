# -*- coding: utf-8 -*-
import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

names=['comments','date','user_id','user_name','user_profile_image_url']

#topics=['八达岭老虎咬人案','女子痛斥医院票贩','西安地铁三号线']
topics=['西安地铁三号线']
for topic in topics:
    idpath="./"+topic+"/id.csv"
    ids=pandas.read_csv(idpath).id
    for id in ids:
        datapath="./{topic}/id{id}-RepostComment.csv".format(topic=topic,id=id)
        df=pandas.read_csv(datapath,names=names,encoding='GBK')
        
        '''日期预处理start'''
        pandas.options.mode.chained_assignment = None 
        for index,date in zip(df.index,df.date):
            if '2016' not in date and '2017' not in date:
                df.loc[index,'date']='2017-'+date
        df.to_csv(datapath,mode='w', header=False,index=False)
        '''日期预处理 end'''
        
        #只保存时间的 年 月 日
        for index,date in zip(df.index,df.date):
            df.loc[index,'date']=date[0:10]
        
        #计算每个日期的转发数并按照日期从小到大排序
        newdf=df.date.value_counts().sort_index()
        newdate=[]
        #转换日期的格式从str为datetime.strptime，用于绘图
        for date in newdf.index:
            newdate.append(datetime.datetime.strptime(date, '%Y-%m-%d'))
        
        dates=mdates.date2num(newdate)
        fig, ax = plt.subplots()
        #设置图片大小
        fig.set_size_inches(18.5, 10.5)
        ax.set_xticks(dates) # Tickmark + label at every plotted point
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        
        ax.plot_date(dates, newdf.values, ls='-', marker='o')
        #ax.set_title('repost number')
        ax.set_ylabel('repost number')
        
        # Format the x-axis for dates (label formatting, rotation)
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        
        #fig.show()
        #保存图片
        picpath="./{topic}/id{id}-RepostComment.png".format(topic=topic,id=id)
        fig.savefig(picpath,dpi=500)
        print("save picture: "+picpath)