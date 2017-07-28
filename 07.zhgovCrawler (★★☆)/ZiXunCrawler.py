# -*- coding: utf-8 -*-
'''
爬取珠海市政府网页（http://www.zhuhai.gov.cn/hd/zxts_44606/tsfk/ ）中关于咨询的内容

具体包含：主题、日期、咨询人、处理单位、处理状态、受理意见
'''
import requests
from bs4 import BeautifulSoup
import pandas
import traceback
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}


def getHTMLText(url,code='utf-8'):
    try:
        print("处理URL:"+url)
        r = requests.get(url, timeout=3000)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        traceback.print_exc()

def getData(basicUrl,maxPage):
    for page in range(1,maxPage+1):
        URL=basicUrl.format(page=page)
        html=getHTMLText(URL)
        soup = BeautifulSoup(html, "html.parser")#解析主页面
        eventsList=soup.find('table',attrs={'class':'listAll'})
        #print(html)
        咨询主题=[]
        咨询日期=[]
        咨询人=[]
        咨询内容=[]
        处理单位=[]
        处理状态=[]
        受理意见=[]
        for event in eventsList.find_all('tr')[1:]:#从第一个tr标签开始解析
            detailsUrl='https://www.zh12345.gov.cn'+event.find('a').get('href')#详细内容链接
            detailsHtml=getHTMLText(detailsUrl)
            #print(detailsHtml)
            soup1=BeautifulSoup(detailsHtml, "html.parser")
            detailList=soup1.find('table',attrs={'class':'detail'}).find_all('td',attrs={'class':'R'})
            咨询主题.append(detailList[0].getText().strip())
            咨询日期.append(detailList[1].getText().strip())
            咨询人.append(detailList[2].getText().strip())
            咨询内容.append(detailList[3].getText().strip())
            处理单位.append(detailList[4].getText().strip())
            处理状态.append(detailList[5].getText().strip())
            if '处理中' in 处理状态:
                受理意见.append('None')
            else:
                受理意见.append(detailList[6].getText().strip())
        contentDF=pandas.DataFrame({
                  '咨询主题':咨询主题,
                  '咨询日期':咨询日期,
                  '咨询人':咨询人,
                  '咨询内容':咨询内容,
                  '处理单位':处理单位,
                  '处理状态':处理状态,
                  '受理意见':受理意见
                  })
        if page==1:
            contentDF.to_csv('咨询数据.csv',mode='w',encoding='GBK',header=True,index=False)
        else:
            contentDF.to_csv('咨询数据.csv',mode='a',encoding='GBK',header=False,index=False)
        print('保存第'+str(page)+'页的数据......')

咨询Url='https://www.zh12345.gov.cn/external/zf/getAllListView.do?pwType=0&type=0&callType=11&orgCode=-1&page={page}'

#******这个参数需要人工指定*********
咨询最大页面数=152
#******这两个参数需要人工指定*********
getData(咨询Url,咨询最大页面数)


