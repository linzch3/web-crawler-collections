# -*- coding: utf-8 -*-
'''
程序功能：绘制问题咨询数量的月份变化图并保存到文件夹中
'''
import pandas
import os
import matplotlib.pyplot as plt
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

folderName="问题咨询数量的一周变化图"
if not os.path.exists(folderName):
    os.mkdir(folderName)
    
for filename in first31files.filename:
    if flag:
        df=pandas.read_csv('./ShenZhen_gov_info/'+ filename,encoding='GBK')
        flag=False
    else:
        df=pandas.read_csv('./ShenZhen_gov_info/'+ filename,names=names,encoding='GBK')
    
    #将日期转换成一周的时间(1 -7 分别代表周一到周末）
    day1_to_day7=[datetime.datetime.strptime(date,'%Y.%m.%d').weekday()+1 for date in df.询问日期]
    #计算每周7天的咨询数目并根据重复数量排序              
    newdf=pandas.DataFrame({'date':day1_to_day7}).date.value_counts().sort_index()
    
    fig, ax = plt.subplots()
    #绘制折线图
    ax.plot(newdf.index,newdf.values, ls='-', marker='o')
    #绘制柱状图
    #ax.bar(newdf.index,newdf.values)
    ax.set_xticks(newdf.index)
    ax.set_xticklabels(['周一','周二','周三','周四','周五','周六','周日'],fontproperties='SimHei',fontsize=15)
    ax.set_title(filename.split('.')[0],fontproperties='SimHei',fontsize=15)
    ax.set_ylabel('问题咨询数量',fontproperties='SimHei',fontsize=15)
    #ax.set_xlabel('一周内的时间',fontproperties='SimHei',fontsize=15)
    #plt.show()

    filepath='问题咨询数量的一周变化图/'+filename.split('.')[0]+'_问题咨询数量的一周变化图.jpg'

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