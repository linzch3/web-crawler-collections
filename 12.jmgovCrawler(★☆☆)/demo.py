# -*- coding: utf-8 -*-
'''
demo:
    
'''
import requests
from bs4 import BeautifulSoup
import re
import traceback
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}


def getHTMLText(url,code='GB2312'):
    cnt=0
    while cnt<=100:
        try:
            print("处理URL:"+url)
            r = requests.get(url,headers=headers,timeout=3000)
            r.raise_for_status()
            #print('编码方式'+r.apparent_encoding)
            r.encoding = code
            return r.text
        except:
            cnt=cnt+1
            traceback.print_exc()
            print('\n\n\n\ntry again....\n\n\n\n')
    print('100 times try,but failed........')
    return None
    
#首页要特殊处理，是：http://www.jiangmen.gov.cn/gzhd/szxxnew/default.html
basicUrl='http://www.jiangmen.gov.cn/gzhd/szxxnew/default_{page}.html'
#得到第一页的源代码
htmlText=getHTMLText(basicUrl.format(page=1))
#得到页面的子链接(一般用正则表达式来提取更快)
detailPattern=re.compile('href=\"\.(/[\dt/_]+\.html)')
#得到当前页面下的所有子页面的链接
detailURLs=['http://www.jiangmen.gov.cn/gzhd/szxxnew'+ id for id in detailPattern.findall(htmlText)]
print(detailURLs)
'''
下面测试单个链接的抓取
'''
testLink1='http://www.jiangmen.gov.cn/gzhd/szxxnew/201706/t20170621_792356.html'
testText=getHTMLText(testLink1)
detail=re.findall('<td height=\"40\" align=\"left\">(.*?)</td>',testText)

print(detail[0].strip('&nbsp;').strip())
print(detail[1].strip('&nbsp;').strip())
print(detail[2].strip('&nbsp;').strip())
print(detail[3].strip('&nbsp;').strip('<p class="lxContent">').strip('</p>').strip())
print(detail[4].strip('&nbsp;').strip())
print(detail[5].strip('&nbsp;').strip())
print(detail[6].strip('&nbsp;').strip('<p class="lxContent">').strip('</p>').strip())

事项标题=[]
事项地点=[]
来信时间=[]
来信内容=[]
答复部门=[]
回复时间=[]
回复内容=[]
事项标题.append(detail[0].strip('&nbsp;').strip())
事项地点.append(detail[1].strip('&nbsp;').strip())
来信时间.append(detail[2].strip('&nbsp;').strip())
来信内容.append(detail[3].strip('&nbsp;').strip('<p class="lxContent">').strip('</p>').strip())
答复部门.append(detail[4].strip('&nbsp;').strip())
回复时间.append(detail[5].strip('&nbsp;').strip())
回复内容.append(detail[6].strip('&nbsp;').strip('<p class="lxContent">').strip('</p>').strip())


'''
下面得到最大页面数
'''

def getMaxPage(basicUrl):
    return 24
print(getMaxPage(basicUrl))
