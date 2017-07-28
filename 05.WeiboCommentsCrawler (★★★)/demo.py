# -*- coding: utf-8 -*-
"""
本程序演示如下操作：抓取微博上一个页面的信息，打印该页面下的
转发评论、转发日期、转发用户id、转发用户的用户名、转发用户的头像链接

可帮助理解WeiboRepostCommentsCrawlerByIds.py和WeiboCommentsCrawlerByIds.py的实现逻辑
"""
import json
import requests

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
#得到网页的html源代码
def getHTMLText(url,Code='utf-8'):
    try:
        r=requests.get(url,headers=headers)
        r.raise_for_status()
        r.encoding=Code
        return r.text
    except:
        return ""

page = 1
weiboId = 4089311604948232
dataURL = 'http://m.weibo.cn/api/statuses/repostTimeline?id=%d&page=%d' % (weiboId, page)

jsonString = getHTMLText(dataURL)   #网页的信息是以JSON格式传输的
jsonObject = json.loads(jsonString)
for data in jsonObject['data']:
    print(data.get('raw_text')+'\n')         #评论在JSON对象的data属性的raw_text属性下
    print(data.get('created_at')+'\n')
    print(data.get('user').get('profile_image_url')+'\n')
    print(data.get('user').get('screen_name')+'\n')
    print(data.get('user').get('id'))


