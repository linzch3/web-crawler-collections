# -*- coding: utf-8 -*-
'''
爬取中山市政府市长信箱（http://www.zs.gov.cn/main/zmhd/）中的所有数据

具体包含：诉求编号、所属部门、诉求类型、处理状态、诉求标题、递交时间、诉求来源、事发地点、诉求内容、回复意见
'''
import requests
from bs4 import BeautifulSoup
import pandas
import traceback
import math
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

def getJsonObject(url,code='utf-8'):
    cnt=0
    while cnt<=100:
        try:
            print("处理URL:"+url)
            r = requests.get(url, timeout=3000)
            r.raise_for_status()
            r.encoding = code
            return r.json()
        except:
            cnt=cnt+1
            traceback.print_exc()
            print('\n\n\n\ntry again....\n\n\n\n')
    print('100 times try,but failed........')
    return None   
    
def getMaxPage(url):
    test=getJsonObject(basicUrl.format(page=1))
    return math.ceil(test['total']/len(test['rows']))#总数目除以每页的数目，再向上取整
    
def getData(basicUrl,maxPage):
    for page in range(829,maxPage+1):
        jsonData=getJsonObject(basicUrl.format(page=page))
        ids=[i['id'] for i in jsonData['rows']]
        诉求编号=[]
        所属部门=[]
        诉求类型=[]
        处理状态=[]
        诉求标题=[]
        递交时间=[]
        诉求来源=[]
        事发地点=[]
        诉求内容=[]
        回复意见=[]
        for id in ids:
            detailsUrl='http://12345.zs.gov.cn/external/zs/petitionDetail.do?id='+str(id)#详细内容链接
            detailsHtml=getHTMLText(detailsUrl)
            #print(detailsHtml)
            soup1=BeautifulSoup(detailsHtml, "html.parser")
            detailList=soup1.find('table',attrs={'class':'talb_slbj_gdxqxin'}).find_all('tr')
            detail1=detailList[1].find_all('td')
            诉求编号.append(detail1[0].getText().strip())
            诉求类型.append(detail1[1].getText().strip())
            处理状态.append(detail1[2].getText().strip())
            
            detail2=detailList[2].find_all('td')
            诉求标题.append(detail2[0].getText().strip())
            递交时间.append(detail2[1].getText().strip())
            诉求来源.append(detail2[2].getText().strip())
            
            detail3=detailList[3].find('td')
            所属部门.append(detail3.getText().strip())
            
            事发地点flag=True
            诉求内容flag=True
            回复意见flag=True
            for detail in detailList[4:]:
                title=detail.find('th')
                if title != None:
                    title=title.getText()
                    if '事发地点' in title:
                        事发地点.append(detail.find('td').getText().strip())
                        事发地点flag=False

                    if '诉求内容' in title:
                        诉求内容.append(detail.find('td').getText().strip())
                        诉求内容flag=False
                
                    if '回复意见' in title:
                        回复意见.append(detail.find('td').getText().strip())
                        回复意见flag=False
 
                    
            if 事发地点flag:
                 事发地点.append("None")
            if 诉求内容flag:
                 诉求内容.append("None")
            if 回复意见flag:
                 回复意见.append("None")       
     
        contentDF=pandas.DataFrame({
                  '诉求编号':诉求编号,
                  '诉求类型':诉求类型,
                  '处理状态':处理状态,
                  '诉求标题':诉求标题,
                  '递交时间':递交时间,
                  '处理状态':处理状态,
                  '所属部门':所属部门,
                  '事发地点':事发地点,
                  '诉求内容':诉求内容,
                  '回复意见':回复意见
                  })
        if page==1:
            contentDF.to_csv('中山市数据.csv',mode='w',encoding='utf-8',header=True,index=False)
        else:
            contentDF.to_csv('中山市数据.csv',mode='a',encoding='utf-8',header=False,index=False)
        print('保存第'+str(page)+'页的数据......')
        
basicUrl='http://12345.zs.gov.cn/external/zs/loadDataMailbox.do?page={page}'
maxPage=getMaxPage(basicUrl)
getData(basicUrl,maxPage)
