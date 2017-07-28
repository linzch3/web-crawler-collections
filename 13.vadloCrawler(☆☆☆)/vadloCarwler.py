# -*- coding:utf-8 -*-
'''
程序功能：爬取http://vadlo.com/cartoons.php上的动漫图片
'''
import re
import requests
import traceback
import os

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}

def getHTMLText(url,code='ascii'):
    print("processing url:"+url)
    r = requests.get(url,headers=headers,timeout=3000)
    r.encoding = code
    return r.text

def getGif(num,pictureName):
    fileName='./photo/{num}.'.format(num=num)+pictureName
    with open(fileName,'wb') as f:
        r = requests.get('http://vadlo.com/Research_Cartoons/'+pictureName,headers=headers,timeout=3000)
        r.raise_for_status()
        f.write(r.content)
        print('save file:'+fileName)
num=1
mkdir('photo')
basicUrl='http://vadlo.com/cartoons.php?id={page}'
pattern=re.compile(r'<img border="0" src="Research_Cartoons/(.*?)"')
#经过测验，实际上网站只有125张不重复图片
while num<=125:
    html=getHTMLText(basicUrl.format(page=num))
    getGif(num,pattern.findall(html)[0])# 得到gif的名字，e.g. ['Boy-I-would-love-to-be-his-pet-cat.gif']
    num = num + 1
print('\n\n\n all jobs are done!')