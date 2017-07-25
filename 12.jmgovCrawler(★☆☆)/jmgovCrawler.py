# -*- coding: utf-8 -*-
'''  
爬取江门市市长信箱网页数据（http://www.jiangmen.gov.cn/gzhd/szxxnew/default.html）
  和江门市网上咨询网页数据（http://www.jiangmen.gov.cn/gzhd/wszxnew/default.html）：

具体包含：事项标题、事项地点、来信时间、来信内容、答复部门、回复时间、回复内容 共7项数据

使用方法：命令行下输入 python jmgovCrawler.py szxx ---> 爬取 江门市市长信箱网页数据
        命令行下输入 python jmgovCrawler.py wszx ---> 爬取 江门市网上咨询网页数据
'''
import requests
from bs4 import BeautifulSoup
import sys
import re
import traceback
import pandas
import time
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}

globalSleepTime_Second=60
def getHTMLText(url,code='GB2312'):
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
    return 24

def getData(firstUrl,basicUrl,subDetailUrl,maxPage,fileEncoding,fileName):
    startPage=0
    endPage=int(maxPage)+1#注意加一
    
    for page in range(startPage,endPage):
        #得到每个页面的源代码
        if page==0:
            htmlText=getHTMLText(firstUrl)
        else:
            htmlText=getHTMLText(basicUrl.format(page=page))
            
        if htmlText==None:
            print('放弃该页面：'+basicUrl.format(page=page))
            continue
        
        #得到当前页面下的所有子页面的链接(通常是用正则表达式+列表生成式得到)
        detailPattern=re.compile('href=\"\.(/[\dt/_]+\.html)')
        detailURLs=[subDetailUrl+ id for id in detailPattern.findall(htmlText)]
        #得到所有子页面的数据
        事项标题=[]
        事项地点=[]
        来信时间=[]
        来信内容=[]
        答复部门=[]
        回复时间=[]
        回复内容=[]
        for detail in detailURLs:
            detailText=getHTMLText(detail)
            detail=re.findall('<td height=\"40\" align=\"left\">(.*?)</td>',detailText)
            事项标题.append(detail[0].strip('&nbsp;').strip())
            事项地点.append(detail[1].strip('&nbsp;').strip())
            来信时间.append(detail[2].strip('&nbsp;').strip())
            来信内容.append(detail[3].strip('&nbsp;').strip('<p class="lxContent">').strip('</p>').strip())
            if len(detail)>4:
                答复部门.append(detail[4].strip('&nbsp;').strip())
                回复时间.append(detail[5].strip('&nbsp;').strip())
                回复内容.append(detail[6].strip('&nbsp;').strip('<p class="lxContent">').strip('</p>').strip())
            else:
                答复部门.append('None')
                回复时间.append('None')
                回复内容.append('None')               
        #保存数据
        contentDF=pandas.DataFrame({
                        'A_事项标题':事项标题,
                        'B_事项地点':事项地点,
                        'C_来信时间':来信时间,
                        'D_来信内容':来信内容,
                        'E_答复部门':答复部门,
                        'F_回复时间':回复时间,
                        'G_回复内容':回复内容
                  })
        if page==startPage:
            contentDF.to_csv(fileName,mode='w',encoding=fileEncoding,header=True,index=False)
        else:
            contentDF.to_csv(fileName,mode='a',encoding=fileEncoding,header=False,index=False)
        print('保存第'+str(int(page)+1)+'页的数据......')   

 
              
firstUrl='http://www.jiangmen.gov.cn/gzhd/{type}new/default.html'.format(type=sys.argv[1])    
url='http://www.jiangmen.gov.cn/gzhd/{type}new'.format(type=sys.argv[1])        
basicUrl=url+'/default_{page}.html' 
maxPage=getMaxPage(basicUrl)
print('最大页面数为'+str(maxPage))
if sys.argv[1]=='szxx':
    fileName='江门市市长信箱数据.csv'
else:
    fileName='江门市网上咨询数据.csv'
getData(firstUrl,basicUrl,url,maxPage,'utf-8',fileName)