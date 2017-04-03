# -*- coding: utf-8 -*-
import time
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import traceback

#得到网页的html源代码
def getHTMLText(url,Code='utf-8'):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=Code
        return r.text
    except:
        return ""

#读取单个网页的 链接（hrefs、 标题（titles）、 发布日期（pdates）
def readList(url):
    do = True
    sleepSecond = 1
    hrefs = []
    titles = []
    pdates = []

    while do:
        time.sleep(sleepSecond)
        try:
            html= getHTMLText(url)
            soup = BeautifulSoup(html,'html.parser')
            ul = soup.find(attrs={"class":"gllist"})
            lis = ul.findAll('li')
            
            for li in lis:
                href = li.find('a').attrs['href']
                title = li.find('a').text
                pdate = li.find('span').text
                hrefs.append(href)
                titles.append(title)
                pdates.append(pdate)
        except :
            traceback.print_exc()
        else:
            do = False
    return (hrefs, titles, pdates)

#读取第一篇网页的 链接（hrefs、 标题（titles）、 发布日期（pdates）
hrefs, titles, pdates = readList('http://www.gd.gov.cn/govpub/xxts/index.htm')

#得到所有网页的页数
html = getHTMLText('http://www.gd.gov.cn/govpub/xxts/index.htm')
pageTag = "var countPage = "
pageStart = html.find(pageTag) + len(pageTag)
pageEnd = pageStart + 2
pages = int(html[pageStart: pageEnd])

#读取剩余网页的 链接（hrefs、 标题（titles）、 发布日期（pdates）
for page in range(1, pages):
    url = 'http://www.gd.gov.cn/govpub/xxts/index_%d.htm' % (page)
    print(url)
    _hrefs, _titles, _pdates = readList(url)
    hrefs.extend(_hrefs)
    titles.extend(_titles)
    pdates.extend(_pdates)

#读取网页的新闻正文
def readPage(url):
    print(url)
    do = True
    sleepSecond = 1
    content = ""

    while do:
        time.sleep(sleepSecond)
        try:
            html= getHTMLText(url)
            soup = BeautifulSoup(html,'html.parser')
            contentDiv = soup.find("div", {'class': 'content'})
            
            if contentDiv == None:
                content = soup.text
            else:
                content = contentDiv.text
        except :
            traceback.print_exc()
        else:
            do = False
    content = content.strip().replace("\n", '')
    return content

#得到所有网页的新闻正文
contents = []
for href in hrefs:
    content = readPage(href)
    contents.append(content)

#将数据保存为ataFrame类型，写入CSV文件
result = DataFrame({
    'href': hrefs, 
    'title': titles, 
    'pdate': pdates,
    'content': contents
})

result.to_csv("result.csv")
