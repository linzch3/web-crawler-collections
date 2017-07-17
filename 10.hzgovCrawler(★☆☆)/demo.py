# -*- coding: utf-8 -*-
'''
demo:
    
爬取惠州市人民政府网页（http://www.huizhou.gov.cn/wlwzlist.shtml?method=letters4bsznList3&pager.offset=0）中关于网络问政的内容

具体包含：来信人、来信主题、受文单位、来信时间、来信类型、办理状态、来信内容、最终回文单位、最终办理时间、最终处理结果 共10项数据
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
            r = requests.get(url, timeout=3000)
            r.raise_for_status()
            r.encoding = code
            return r.text
        except:
            cnt=cnt+1
            traceback.print_exc()
            print('\n\n\n\ntry again....\n\n\n\n')
    print('100 times try,but failed........')
    return None
    
basicURL='http://www.huizhou.gov.cn/wlwzlist.shtml?method=letters4bsznList3&pager.offset={step}'
#得到首页的源代码
text=getHTMLText(basicURL.format(step=0))#step从0开始 每次加20
pattern='method=viewLetter&lid=(.*)\''
#得到页面的子链接
detailURLs=['http://www.huizhou.gov.cn/viewletter.shtml?method=viewLetter&lid='+ id for id in re.findall(pattern,text)]
print("当前页面的子链接：")
print(detailURLs)


'''
下面测试单个链接的抓取
'''
#已办理 -5
testLink1='http://www.huizhou.gov.cn/viewletter.shtml?method=viewLetter&lid=ff8080815cdec039015d4025c4d800e4'
#办理中 -2
testLink2='http://www.huizhou.gov.cn/viewletter.shtml?method=viewLetter&lid=ff8080815cdec039015d3c01bd5d676e'
#已转入 -2
testLink3='http://www.huizhou.gov.cn/viewletter.shtml?method=viewLetter&lid=ff8080815cdec039015d3af653d25e20'
#转其他部门 -5
testLink4='http://www.huizhou.gov.cn/viewletter.shtml?method=viewLetter&lid=ff8080815cdec039015d3c85a5706786'
#转其他部门 -3 len4
testLink5='http://www.huizhou.gov.cn/viewletter.shtml?method=viewLetter&lid=ff8080815cdec039015d3af465c25e1e'
testText=getHTMLText(testLink4)
soup1=BeautifulSoup(testText, "html.parser")
detailList=soup1.find_all('table',
                          attrs={'width':'100%',
                                 'border':'0',
                                 'cellpadding':'3',
                                 'cellspacing':'5'})
for i in range(0,len(detailList)):
    print(len(detailList[i].find_all('td')))  



#咨询的问题

for i in detailList[0].find_all('td')[1::2]:
        print(i.getText().strip())
        
#最终的回复 已经办理的 和 正在处理的 最终回复需要区分对待

#已经办理完成的
for i in detailList[-5].find_all('td')[1::2]:
        print(i.getText().strip())
 
#正在处理的
for i in detailList[-5].find_all('td'):
        print(i.getText().strip())
        break


      
#得到最大页面数
maxPagePattern=r'offset=(.*)\"><nobr>\[末页\]</nobr>'
re.findall(maxPagePattern,text)    

def getMaxPage(url):
    test=getHTMLText(basicURL.format(step=0))
    maxPagePattern=r'offset=(.*)\"><nobr>\[末页\]</nobr>'
    return re.findall(maxPagePattern,test)[0]    
    
print(getMaxPage(basicURL))  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




