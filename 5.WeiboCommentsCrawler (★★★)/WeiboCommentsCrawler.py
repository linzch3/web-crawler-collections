# -*- coding: utf-8 -*-
"""
说明：可通过添加特定单条首条微博的id到weiboIds.csv，程序会抓取该文件设定的id的数据
需要注意：在初次运行该代码时，必须保证completed.csv里面只有两行数据(第一行为：page,pagesId 第二行为空行)
"""
import time
import json
import numpy
import pandas
import requests
import traceback

commonAPI = 'http://m.weibo.cn/api/statuses/repostTimeline?id=%d&page=%d'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

#得到网页的html源代码
def getHTMLText(url,Code='utf-8'):
    try:
        r=requests.get(url,headers=headers)
        r.raise_for_status()
        r.encoding = Code
        return r.text
    except:
        return ""
        
##得到网页对应的JSON对象
def getJSONObject(weiboId, page):
    do = True
    sleepSecond = 1
    jsonObject = ""

    while do:
        time.sleep(sleepSecond)
        dataURL = commonAPI % (weiboId, page)
        print("处理 URL: %s" % (dataURL))

        jsonString = getHTMLText(dataURL)
        jsonObject = json.loads(jsonString)
    
        if 'data' not in jsonObject:
            sleepSecond = sleepSecond+5
            print("遭受限制~~~，%s 秒后重试" % (sleepSecond))
        else :
            do = False
    
    return jsonObject

#可通过添加话题的id到weiboIds.csv中，
weiboIds = pandas.read_csv("weiboIds.csv").weiboId

"""
    准备好要处理的页面链接需要的id和page ----start
"""
pagesIds = [] #页面的id
pages = []    #页面所在页数
for pid in weiboIds:
    page = 1
    jsonObject = getJSONObject(pid, page) #得到话题的第一页
    totalPage = jsonObject['max']         #话题下的页面总数
    for page in range(1, totalPage+1):    #
        pagesIds.append(pid)
        pages.append(page)
        

allNeed = pandas.DataFrame({'pagesId':pagesIds, 'page':pages})

allNeed.to_csv("allNeed.csv", index=False)

"""
     准备好要处理的页面链接需要的id和page ----end    
"""

#要完成的工作
allNeed = pandas.read_csv("allNeed.csv",dtype=(numpy.int64, numpy.int64))
#已经完成的工作(注意：completed.csv这个文件要事先建好)
completed = pandas.read_csv("completed.csv",dtype=(numpy.int64, numpy.int64))
#待完成的工作
needToGet = allNeed[pandas.DataFrame.all(~allNeed.isin(completed),axis=1)]

while needToGet.size>0:
    completedPagesIds = []
    completedPages = []
    for index, row in needToGet.iterrows():
        pid = row['pagesId']    
        page = row['page']
        
        try:
            contents = []
            jsonObject = getJSONObject(pid, page)
            
            #评论在得到的JSON对象的data属性中
            comments = jsonObject['data']      
            #将评论添加到contents中
            for comment in comments:
                contents.append(comment['raw_text'])
            
            #将完成爬取的评论添加到content.csv中
            contentDF = pandas.DataFrame({'contents': contents})    
            contentDF.to_csv(
                'content.csv',
                mode='a', header=False, index=False
            )
            #记录已经完成的工作
            completedPagesIds.append(pid)
            completedPages.append(page)
        except:
            traceback.print_exc()
            
    #更新allNeed、completed、needToGet
    newCompleted = pandas.DataFrame(
        {'pagesId':completedPagesIds, 'page':completedPages}, 
        dtype=(numpy.int64, numpy.int64))
    
    newCompleted.to_csv(
        "completed.csv",
        mode='a', header=False, index=False)
    
    completed = pandas.read_csv(
        "completed.csv",
        dtype=(numpy.int64, numpy.int64))
    
    needToGet = allNeed[pandas.DataFrame.all( ~allNeed.isin(completed), axis=1)]