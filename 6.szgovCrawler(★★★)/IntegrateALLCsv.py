# -*- coding: utf-8 -*-
'''
程序功能: 用pandas将多个同格式csv数据文件合并
    
注意点：
1.文件编码问题：

windows系统excel另存的csv文件可以用pandas的encoding='gbk'来读写，对中文就可以很好的支持。

python默认的'utf-8'编码的csv文件，excel打开中文是乱码

'''
import pandas
import os

#names=['number','title','inbox','askDate','replyDate','askContents','replyContents']
names=['编号','标题','接收信箱','询问日期','回复日期','询问内容','回复内容']
for index,filename in enumerate(os.listdir('./ShenZhen_gov_info')):
    file=pandas.read_csv('./ShenZhen_gov_info/'+filename,names=names,encoding='GBK')
    if index==0:
        file.to_csv("整合的所有信息.csv",encoding='GBK',mode='w', header=True,index=False)
    else:
        file.to_csv("整合的所有信息.csv",encoding='GBK',mode='a', header=False,index=False)
    print("merge:"+filename)