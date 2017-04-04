# -*- coding: utf-8 -*-
import time
import json
import pandas
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import os
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
#得到网页的html源代码
def getHTMLText(url,Code='utf-8'):
    try:
        r=requests.get(url,headers=headers)
        r.raise_for_status()
        r.encoding = Code
        return r.text
    except:
        return ""
        
def getJSONObject(keyword, page):
    do = True
    sleepSecond = 1
    jsonObject = ""

    while do:
        time.sleep(sleepSecond)
        keyword = quote(keyword)
        dataURL = 'http://m.weibo.cn/container/getIndex?type=all&queryVal=%s&luicode=10000011&lfid=100103type%%3D1%%26q%%3D%s&title=%s&containerid=100103type%%3D1%%26q%%3D%s&page=%d' % (keyword, keyword, keyword, keyword, page)

        print("处理 URL: %s" % (dataURL))
        
        jsonString = getHTMLText(dataURL)
        jsonObject = json.loads(jsonString)
    
        if 'cards' not in jsonObject:
            sleepSecond = sleepSecond+5
            print("遭受限制~~~，%s 秒后重试" % (sleepSecond))
            continue
        else :
            do = False
    
    return jsonObject

page = 0
keyword = '中山大学'#需要指定的keyword

do = True
weiboIds = []
weiboTexts = []
pics = []  #保存图片的链接
while do:
    print("page:" + chr(page))
    resultObject = getJSONObject(keyword, page)
    cards = resultObject['cards']
    if len(cards)==0:
            do = False
            continue
    for card in cards:
        cardGroups = card['card_group']
        
        for group in cardGroups:
            if 'mblog' in group:
                html = group['mblog']['text']
                soup = BeautifulSoup(html,'html.parser')
                weiboId = group['mblog']['id']
                weiboIds.append(weiboId)
                weiboTexts.append(soup.text)
                #pic = ""
                #if 'pics' in group['mblog']:
                #    pices = group['mblog']['pics']
                #    pic = pices[0]['url']
                #pics.append(pic)
    page = page + 1
    
data = pandas.DataFrame({
    'id': weiboIds,
    'text': weiboTexts,
    #'pics': pics #保存图片链接
})

if not os.path.exists("outputFiles"):
    os.mkdir("outputFiles")
    
data.to_csv("outputFiles/weibo_search_" + keyword + ".csv", encoding='utf-8', index=False)