# -*- coding: utf-8 -*-
'''
程序功能：绘制问题咨询数量的年度变化图并保存到文件夹中
'''
import pandas
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

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
folderName="问题咨询数量的年份变化图"
if not os.path.exists(folderName):
    os.mkdir(folderName)
    
for filename in first31files.filename:
    if flag:
        df=pandas.read_csv('./ShenZhen_gov_info/'+ filename,encoding='GBK')
        flag=False
    else:
        df=pandas.read_csv('./ShenZhen_gov_info/'+ filename,names=names,encoding='GBK')
    #截取日期的年份信息
    date=[date[0:4] for date in df.询问日期]
    #计算每年的咨询数目并根据重复数量排序
    newdf=pandas.DataFrame({'date':date}).date.value_counts().sort_index()

    newdate=[]
    #转换日期的格式从str为datetime.strptime，用于绘图
    for date in newdf.index:
        newdate.append(datetime.datetime.strptime(date, '%Y'))
    
    dates=mdates.date2num(newdate)
    fig, ax = plt.subplots()
    #设置图片大小
    #fig.set_size_inches(18.5, 10.5)
    ax.set_xticks(dates) # Tickmark + label at every plotted point
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    ax.plot_date(dates, newdf.values, ls='-', marker='o')
    ax.set_title(filename.split('.')[0],fontproperties='SimHei',fontsize=15)
    ax.set_ylabel('咨询问题数量',fontproperties='SimHei',fontsize=15)
    ax.set_xlabel('年份',fontproperties='SimHei',fontsize=15)
    
    # Format the x-axis for dates (label formatting, rotation)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
        
    #plt.show()
    filepath='问题咨询数量的年份变化图/'+filename.split('.')[0]+'_问题咨询数量的年份变化图.jpg'
    
    plt.savefig(filepath)
    plt.cla()
    plt.close(fig)
    '''
       实际上上面的3行代码可以用： fig.savefig(filepath) 代替，但是后者有个缺点是
       可能在运行的时候报如下错误：
       
       RuntimeWarning: More than 20 figures have been opened. Figures
       created through the pyplot interface (`matplotlib.pyplot.figure`) 
       are retained until explicitly closed and may consume too much memory.
       (To control this warning, see the rcParam `figure.max_open_warning`).
       max_open_warning, RuntimeWarning)
    
    '''
    print('save file: '+filepath)
