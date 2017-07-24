# -*- coding: utf-8 -*-
'''  
爬取肇庆市政府网页（http://wz.zhaoqing.gov.cn/wzpt/index.php?act=political&op=political_list1&curpage=0）中关于网友问政的内容

具体包含：问政标题、 网友名称、问政日期、浏览次数、问政内容、回复内容、牵头部门 共7项数据
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
            #globalSleepTime_Second+=120
            time.sleep(globalSleepTime_Second)
            print('\n\n\n\ntry again....\n\n\n\n')
    print('100 times try,but failed........')
    return None
    
def getMaxPage(basicUrl):
    print('预处理阶段：得到最大页面数')
    test=getHTMLText(basicUrl.format(page=0))
    maxPagePattern=r'curpage=(\d+)\"><span>末页</span>'
    return re.findall(maxPagePattern,test)[0]

def getData(basicUrl,maxPage,fileEncoding):
    startPage=1
    endPage=int(maxPage)+1#注意加一
    
    for page in range(93,endPage):
        #得到每个页面的源代码
        htmlText=getHTMLText(basicUrl.format(page=page))
        if htmlText==None:
            print('放弃该页面：'+basicUrl.format(page=page))
            continue

        #得到页面的子链接(一般用正则表达式来提取更快)
        detailPattern=re.compile('political_id=(\d+)')
        #得到当前页面下的所有子页面的链接
        detailUrls=['http://wz.zhaoqing.gov.cn/wzpt/index.php?act=political&op=political_content&political_id='+ id for id in detailPattern.findall(htmlText)[::2]]
        #得到所有子页面的数据
        问政标题=[]
        网友名称=[]
        问政日期=[]
        浏览次数=[]
        问政内容=[]
        回复内容=[]
        牵头部门=[]

        #牵头部门
        soup=BeautifulSoup(htmlText, "html.parser")
        department=soup.find_all('a',
                                  attrs={'style':'color:black;text-align: right'})
        牵头部门=[i.getText().strip() for i in department]
        for detail in detailUrls:
            detailText=getHTMLText(detail)
            soup1=BeautifulSoup(detailText, "html.parser")
            questionDetail=soup1.find('div',
                                      attrs={'class':'timeline-body-head'})
            #问政标题
            问政标题.append(questionDetail.find('h2').getText().strip())
            #网友名称
            网友名称.append(questionDetail.find_all('font')[0].getText().strip())
            #问政日期
            问政日期.append(questionDetail.find_all('font')[1].getText().strip())
            #浏览次数
            浏览次数.append(questionDetail.find_all('font')[2].getText().strip())
            
            contentDetail=soup1.find_all('div',
                                      attrs={'class':'liuyan_user_text'})
            #问政内容
            问政内容.append(contentDetail[0].getText().strip())
            
            #回复内容
            if len(contentDetail)==2:
                回复内容.append(contentDetail[1].getText().strip())
            else:
                回复内容.append('待回复')
        #保存数据
        contentDF=pandas.DataFrame({
                        'A_问政标题':问政标题,
                        'B_网友名称':网友名称,
                        'C_问政日期':问政日期,
                        'D_浏览次数':浏览次数,
                        'E_问政内容':问政内容,
                        'F_回复内容':回复内容,
                        'G_牵头部门':牵头部门
                  })
        if page==startPage:
            contentDF.to_csv('肇庆市问政数据.csv',mode='w',encoding=fileEncoding,header=True,index=False)
        else:
            contentDF.to_csv('肇庆市问政数据.csv',mode='a',encoding=fileEncoding,header=False,index=False)
        print('保存第'+str(int(page))+'页的数据......')   
               
        
basicUrl='http://wz.zhaoqing.gov.cn/wzpt/index.php?act=political&op=political_list1&curpage={page}'
maxPage=getMaxPage(basicUrl)
print('最大页面数为'+str(maxPage))
getData(basicUrl,maxPage,'utf-8')