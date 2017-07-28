# -*- coding: utf-8 -*-
'''  
爬取xxxx网页（xxx）中关于xxx的内容

具体包含：xxx 共xxx项数据
'''
import requests
from bs4 import BeautifulSoup
import re
import traceback
import pandas
import time
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}

globalSleepTime_Second=60
def getHTMLText(url,code='utf-8'):
    cnt=0
    global globalSleepTime_Second
    while cnt<=100:
        try:
            print("处理URL:"+url)
            r = requests.get(url,headers=headers,timeout=3000)
            r.raise_for_status()
            r.encoding = code
            return r.text
        except:
            cnt=cnt+1
            traceback.print_exc()
            #globalSleepTime_Second+=120
            time.sleep(globalSleepTime_Second)
            print('\n\n\n\ntry again....\n\n\n\n')
    print('100 times try,but failed........')
    return None
    
def getMaxPage(basicUrl):
    print('预处理阶段：得到最大页面数')
    pass

def getData(basicUrl,maxPage,fileEncoding):
    startPage=0
    endPage=int(maxPage)+1#注意加一
    
    for page in range(startPage,endPage):
        #得到每个页面的源代码
        htmlText=getHTMLText(basicUrl.format(page=page))
        if htmlText==None:
            print('放弃该页面：'+basicUrl.format(page=page))
            continue

        #得到当前页面下的所有子页面的链接(通常是用正则表达式+列表生成式得到)
       
        #得到所有子页面的数据
        '''
        标题=[]
        内容=[]
        '''
        #保存数据
        contentDF=pandas.DataFrame({
                 '''
                 'A_标题':标题,
                 'B_内容':内容
                 '''
                  })
        if page==startPage:
            contentDF.to_csv('xxx.csv',mode='w',encoding=fileEncoding,header=True,index=False)
        else:
            contentDF.to_csv('xxx.csv',mode='a',encoding=fileEncoding,header=False,index=False)
        print('保存第'+str(int(page/20)+1)+'页的数据......')   
               
        
basicUrl='xxx{page}'
maxPage=getMaxPage(basicUrl)
print('最大页面数为'+str(maxPage))
getData(basicUrl,maxPage,'utf-8')