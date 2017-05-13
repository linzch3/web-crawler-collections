# -*- coding: utf-8 -*-
'''
程序功能：爬取 深圳市政府在线网站（http://www.sz.gov.cn/cn/hdjl/zxts/dfyjcx/）

的在线咨询投诉公开问题的相关信息

注意：若想爬取当前时间该网站的此类数据，应根据上面的网站找到最大的页面数pageNum=记录条数除以10的值向上取整

'''
import requests
from bs4 import BeautifulSoup
import pandas
import traceback
import os
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}

globalSession=requests.Session()#全局会话对象
'''
【重要】：全局会话对象一定要先声明，否则根据主页面（根据basicUrl得到的页面）爬取的对应详细内容的子页面链接会失效（

此时得到的页面源代码为：
<meta charset="utf-8" content="width=device-width, initial-scale=1.0, maximum-scale=1.0;" name="viewport">
<center>参数已过期！请刷新父页面重试。</center>
<center>或将浏览器设置为接收所有Cookie。</center>
</meta>

）

知识点：

在之前的代码中使用：

r = requests.get(url, timeout=30)
 
的请求中，每次请求其实都相当于发起了一个新的请求。

也就是相当于我们每个请求都用了【不同的浏览器】单独打开的效果。

也就是它并不是指的【一个会话】，即使请求的是同一个网址。

错误分析：

之前没加全局会话对象出现的问题就是：

用程序得到主页面的源码之后，解析出来的本应对应子页面的链接会失效，具体是链接上的参数r会变化。

对于同一个详细内容子页面（从documentid都为6673202可知是同一个），程序在运行时每次请求得到的连接都不一样

http://61.144.227.212/was5/web/zxts_detail.jsp?documentid=6673202&r=1627431734

URL:http://61.144.227.212/was5/web/zxts_detail.jsp?documentid=6673202&r=1309118305

http://61.144.227.212/was5/web/zxts_detail.jsp?documentid=6673202&r=2019654154

观察发现，就是链接上的r参数发生了变化。

关于这点发现，可通过如下操作检验：

1.在浏览器1打开一个详细内容子页面的链接，比如http://61.144.227.212/was5/web/zxts_detail.jsp?documentid=6673202&r=1627431734，

2.将上一步得到的链接用另外一个浏览器打开，这时会发现，页面显示的就是“参数已过期！请刷新父页面重试。或将浏览器设置为接收所有Cookie。”的信息。

'''
def getHTMLText(url,code='utf-8'):
    try:
        print("处理URL:"+url)
        r = globalSession.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        traceback.print_exc()

#页面URL
basicUrl='http://61.144.227.212/was5/web/search?page={page}&channelid=202091&perpage=10&outlinepage=5'

pageNum=3390#最大页面数
if not os.path.exists("ShenZhen_gov_info"):
    os.mkdir("ShenZhen_gov_info")
    
for page in range(1,pageNum+1):
    URL=basicUrl.format(page=page)
    html=getHTMLText(URL)
    
    soup = BeautifulSoup(html, "html.parser")#解析主页面
    eventsList=soup.find('div',attrs={'class':'zx_ml_list zx_hd_list'})
    for event in eventsList.find_all('li')[1:]:#从第一个li标签·开始解析
        numbers=[]#编号
        titles=[]#标题
        inboxs=[]#接收信箱
        askDate=[]#提问日期
        replyDate=[]#回复日期
        askContents=[]#提问内容
        replyContens=[]#回复内容
        try:
            numbers.append(event.find('span',attrs={'class':'number'}).getText())
            
            allATags=event.find_all('a')
            titles.append(allATags[0].get("title"))
            inboxs.append(allATags[1].getText())
            
            #print(allATags)
            detailsUrl='http://61.144.227.212'+allATags[0].get("href")#详细内容链接
            #print(detailsUrl)
            detailsHtml=getHTMLText(detailsUrl)
            soup1 = BeautifulSoup(detailsHtml, "html.parser")
            #print(soup1)
            detailsList=soup1.find('table',attrs={'class':'publicTable'}).find_all('div',attrs={'align':'left'})
            
            askContents.append(detailsList[4].getText())#提问内容
            
            replyContens.append(detailsList[5].getText())#回复内容
            
            allSpanTags=event.find_all('span');
            askDate.append(allSpanTags[-2].getText())
            replyDate.append(allSpanTags[-1].getText())
            
            contentDF=pandas.DataFrame({
            'a_number':numbers,
            'b_title':titles,
            'c_inbox':inboxs,
            'd_askDate':askDate,
            'e_replyDate':replyDate,
            'f_askContents':askContents,
            'g_replyContens':replyContens
            })
            
            #将数据按 接受信箱 分类保存
            fileName='ShenZhen_gov_info/'+inboxs[0]+'.csv'
            contentDF.to_csv(fileName,mode='a', header=False,index=False)
        except:
            traceback.print_exc()
        
        