# -*- coding: utf-8 -*-
"""
程序功能：可通过添加特定单条首条微博的id到weiboIds.csv，程序会抓取对应id的
转发评论、转发日期、转发用户id、转发用户的用户名、转发用户的头像链接 5个子信息

需要注意：在初次运行该代码时，必须保证completed.csv里面只有两行数据
(第一行为：page,pagesId 第二行为空行)
"""
import time
import json
import numpy
import pandas
import requests
import traceback
import os

commonRepostAPI = 'http://m.weibo.cn/api/statuses/repostTimeline?id=%d&page=%d'

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
def getJsonObject(weiboId, page,Code='utf-8'):
    cnt=0
    url = commonRepostAPI % (weiboId, page)
    while cnt<=100:
        try:
            print("处理URL:"+url)
            r = requests.get(url, headers=headers, timeout=3000)
            r.raise_for_status()
            r.encoding = Code
            return r.json()
        except:
            cnt=cnt+1
            traceback.print_exc()
            print('\n\n\n\ntry again....\n\n\n\n')
    print('100 times try,but failed........')
    return None 

#可通过添加话题的id到weiboIds.csv中，
weiboIds = pandas.read_csv("weiboIds.csv").weiboId

"""
    准备好要处理的页面链接需要的id和page ----start
"""
pagesIds = [] #页面的id
pages = []    #页面所在页数
print("预处理阶段 开始")
for pid in weiboIds:
    page = 1
    jsonObject = getJsonObject(pid, page) #得到话题的第一页
    totalPage = jsonObject['max']         #话题下的页面总数
    for page in range(1, totalPage+1):    
        pagesIds.append(pid)
        pages.append(page)
        
print("预处理阶段 结束\n\n正式开始数据抓取")

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

if not os.path.exists("outputFiles"):
    os.mkdir("outputFiles")
    
while needToGet.size>0:
    completedPagesIds = []
    completedPages = []
    for index, row in needToGet.iterrows():
        pid = row['pagesId']    
        page = row['page']
        
        try:
            comments = []#转发后附上的评论
            date=[]      #转发日期
            user_id=[]   #转发用户的id
            user_name=[] #转发用户的用户名
            user_profile_image_url=[] #转发用户的头像链接

            jsonObject = getJsonObject(pid, page)
            
            for data in jsonObject['data']:
                comments.append(data.get('raw_text'))      
                date.append(data.get('created_at'))

                user_name.append(data.get('user').get('screen_name'))
                user_id.append(data.get('user').get('id'))
                user_profile_image_url.append(data.get('user').get('profile_image_url'))

            #将完成爬取的数据添加到content.csv中
            contentDF = pandas.DataFrame({
            'date':date,
            'user_id':user_id,
            'user_name':user_name,
            'user_profile_image_url':user_profile_image_url,
            'comments': comments
            })    
            contentFileName='outputFiles/id'+str(pid)+'-RepostComment.csv'
            contentDF.to_csv(
                contentFileName,
                mode='a', header=False,index=False
            )
            #记录已经完成的工作
            completedPagesIds.append(pid)
            completedPages.append(page)
        except:
            traceback.print_exc()
            
    #更新allNeed、completed、needToGet
    newCompleted = pandas.DataFrame({
                  'pagesId':completedPagesIds,
                  'page':completedPages}, 
                  dtype=(numpy.int64, numpy.int64))
    
    newCompleted.to_csv(
        "completed.csv",
        mode='a', header=False, index=False)
    
    completed = pandas.read_csv(
        "completed.csv",
        dtype=(numpy.int64, numpy.int64))
    
    needToGet = allNeed[pandas.DataFrame.all( ~allNeed.isin(completed), axis=1)]