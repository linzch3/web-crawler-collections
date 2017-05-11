# -*- coding: utf-8 -*-
'''
程序功能：获取代理ip，服务爬虫程序
参考博客：http://www.cnblogs.com/hearzeus/p/5157016.html
实现效果：从http://api.xicidaili.com/free2016.txt这里得到的IP 100个中基本上有3-8个可以用，效果不好。
不过，本代码整体框架思路还是可以参考的。
'''
import requests

#调用API得到IP
r=requests.get('http://api.xicidaili.com/free2016.txt')
with open('test.txt','wb') as f:
    f.write(r.content)
 
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
proxys = []
with open('test.txt','r',encoding='utf-8') as f:
    for i in f.readlines():
        host='http://'+i.strip('\n')
        proxys.append({'http':host})

dataURL = 'http://ip.chinaz.com/getip.aspx'
#测试代理IP
for proxy in proxys:
    try:
        print("尝试测试代理IP:",end="")
        print(proxy['http'])
        
        r=requests.get(dataURL,
                       headers=headers,
                       proxies=proxy,
                       timeout=3)
        print(len(r.text))
    except Exception as e:
        print("failed")
        continue
    
    
    
