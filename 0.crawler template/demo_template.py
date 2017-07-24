# -*- coding: utf-8 -*-
'''
demo:
    
'''
import requests
from bs4 import BeautifulSoup
import re
import traceback
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}


def getHTMLText(url,code='utf-8'):
    cnt=0
    while cnt<=100:
        try:
            print("处理URL:"+url)
            r = requests.get(url,headers=headers,timeout=3000)
            r.raise_for_status()
            print('编码方式'+r.apparent_encoding)#注意判断编码方式
            r.encoding = code
            return r.text
        except:
            cnt=cnt+1
            traceback.print_exc()
            print('\n\n\n\ntry again....\n\n\n\n')
    print('100 times try,but failed........')
    return None
    
basicUrl='xxx{page}'
#得到首页的源代码
htmlText=getHTMLText(basicUrl.format(page=0))
#得到页面的子链接(一般用正则表达式来提取更快)
detailPattern=re.compile('political_id=(\d)+')
#得到当前页面下的所有子页面的链接
detailURLs=['http://www.huizhou.gov.cn/viewletter.shtml?method=viewLetter&lid='+ id for id in detailPattern.findall(htmlText)]

'''
下面测试单个链接的抓取
'''
testLink1=''
testText=getHTMLText(testLink1)
soup1=BeautifulSoup(testText, "html.parser")
detailList=soup1.find_all('table',
                          attrs={'width':'100%',
                                 'border':'0',
                                 'cellpadding':'3',
                                 'cellspacing':'5'})
#balabala

'''
下面得到最大页面数
'''

def getMaxPage(basicUrl):
    print('预处理阶段：得到最大页面数')
    test=getHTMLText(basicUrl.format(page=0))
    '''
    使用正则表达式得到 末页 对应的最大页面
    方法：查看源代码->搜素 末页
    注意点：正则表达式要尽量精确，对于匹配最大页面数，使用\d+来匹配相对.*?就比较精确
    '''
    maxPagePattern=r'curpage=(\d+)\"><span>末页</span>'
    return re.findall(maxPagePattern,test)[0]
print(getMaxPage(basicUrl))
