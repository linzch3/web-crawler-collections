# -*- coding:utf-8 -*-
#for details, see:http://blog.csdn.net/linzch3/article/details/62273278
import requests
from bs4 import BeautifulSoup
import bs4
import re

def getHTMLText(inputIP,url):
    try:
        kv = {'ip': inputIP}
        r = requests.get(url,params=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Failed!")

def getData(html):
    data=[]
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find_all('tr'):
        if isinstance(tr, bs4.element.Tag):  # 过滤掉非标签类型
            lis = tr('li')  #取出tr标签的li标签，若tr标签没有li标签，则lis为None
            if(lis!=None):
                data+=[i.string for i in lis]#去除标签，得到数据
    return data

url = "http://www.ip138.com/ips138.asp"
inputIP=input('请输入IP地址：')
html=getHTMLText(inputIP,url)
data=getData(html)
for i in data:
    print(i)
