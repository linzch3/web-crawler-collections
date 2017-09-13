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
'''
另外有个类似的网站可以查询ip地址对应在地球的位置：

使用方法：http://freegeoip.net/json/ + 你的ip地址 进行GET请求后可得到一个json数据。

比如：http://freegeoip.net/json/120.236.174.148

{"ip":"120.236.174.148","country_code":"CN","country_name":"China","region_code":"44","region_name":"Guangdong","city":"Guangzhou","zip_code":"","time_zone":"Asia/Shanghai","latitude":23.1167,"longitude":113.25,"metro_code":0}

就是我的ip地址所在地区了。相比代码测试的那个网站，这个网站提供的数据更为精确和丰富。
'''
