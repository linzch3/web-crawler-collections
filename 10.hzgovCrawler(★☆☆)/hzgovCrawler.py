# -*- coding: utf-8 -*-
'''  
爬取惠州市人民政府网页（http://www.huizhou.gov.cn/wlwzlist.shtml?method=letters4bsznList3&pager.offset=0）中关于网络问政的内容

具体包含：来信人、来信主题、受文单位、来信时间、来信类型、办理状态、来信内容、最终回文单位、最终办理时间、最终处理结果 共10项数据
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
            r = requests.get(url, timeout=3000)
            r.raise_for_status()
            r.encoding = code
            return r.text
        except:
            cnt=cnt+1
            traceback.print_exc()
            globalSleepTime_Second+=120
            time.sleep(globalSleepTime_Second)
            print('\n\n\n\ntry again....\n\n\n\n')
    print('100 times try,but failed........')
    return None
    
def getMaxPage(basicUrl):
    print('预处理阶段：得到最大页面数')
    test=getHTMLText(basicUrl.format(step=0))
    maxPagePattern=r'offset=(.*)\"><nobr>\[末页\]</nobr>'
    maxPage=re.findall(maxPagePattern,test)[0]
    print('最大页面数为'+str(maxPage))
    return maxPage    
    
def getData(basicUrl,maxPage,fileEncoding):
    startPage=0
    endPage=int(maxPage)+1#注意加一
    cnt=0#爬取页面计数器
    #1100
    for page in range(startPage,endPage,20):#步长为20
        #得到每个页面的源代码
        htmlText=getHTMLText(basicUrl.format(step=page))
        if htmlText==None:
            continue
        detailPattern=re.compile('method=viewLetter&lid=(.*)\'')
        #得到当前页面下的所有子页面的链接
        detailURLs=['http://www.huizhou.gov.cn/viewletter.shtml?method=viewLetter&lid='+ id for id in detailPattern.findall(htmlText)]
        来信人=[]
        来信主题=[]
        受文单位=[]
        来信时间=[]
        来信类型=[]
        办理状态=[]
        来信内容=[]
        最终回文单位=[]
        最终办理时间=[]
        最终处理结果=[]
        #得到所有子页面的数据
        for detail in detailURLs:
            detailPage=getHTMLText(detail)
            if detailPage==None:
                continue
            soup1=BeautifulSoup(detailPage, "html.parser")
            detailList=soup1.find_all('table',
                                      attrs={'width':'100%',
                                             'border':'0',
                                             'cellpadding':'3',
                                             'cellspacing':'5'})
            #咨询的问题
            question=detailList[0].find_all('td')[1::2]
            来信人.append(question[0].getText().strip())
            来信主题.append(question[1].getText().strip())
            受文单位.append(question[2].getText().strip())
            来信时间.append(question[3].getText().strip())
            来信类型.append(question[4].getText().strip())        
            办理状态.append(question[5].getText().strip())  
            来信内容.append(question[6].getText().strip())  
            
#            #最终的回复 需要根据是否处于 正在办理中 状态区分对待
#            if '办理中' in question[5].getText().strip():
#                reply=detailList[-2].find_all('td')[1::2]
#            elif '已转入' in question[5].getText().strip():
#                reply=detailList[-2].find_all('td')[1::2]
#            else:
#                reply=detailList[-5].find_all('td')[1::2]

            for detail in detailList[::-1]:
                tmp=detail.find_all('td')
                if(len(tmp)==6 and tmp[0].getText().strip()=='回文单位'):
                    reply=tmp[1::2]
            
            最终回文单位.append(reply[0].getText().strip())
            最终办理时间.append(reply[1].getText().strip())
            最终处理结果.append(reply[2].getText().strip())
            

        #保存数据
        contentDF=pandas.DataFrame({
                  'A来信人':来信人,
                  'B来信主题':来信主题,
                  'C受文单位':受文单位,
                  'D来信时间':来信时间,
                  'E来信类型':来信类型,
                  'F办理状态':办理状态,
                  'G来信内容':来信内容,
                  'H最终回文单位':最终回文单位,
                  'I最终办理时间':最终办理时间,
                  'J最终处理结果':最终处理结果
                  })
        if page==startPage:
            contentDF.to_csv('惠州市数据.csv',mode='w',encoding=fileEncoding,header=True,index=False)
        else:
            contentDF.to_csv('惠州市数据.csv',mode='a',encoding=fileEncoding,header=False,index=False)
        print('保存第'+str(int(page/20)+1)+'页的数据......')   
        cnt=(cnt+1)%100
        if cnt==99:
            time.sleep(1)              
        
basicUrl='http://www.huizhou.gov.cn/wlwzlist.shtml?method=letters4bsznList3&pager.offset={step}'
maxPage=getMaxPage(basicUrl)
getData(basicUrl,maxPage,'utf-8')