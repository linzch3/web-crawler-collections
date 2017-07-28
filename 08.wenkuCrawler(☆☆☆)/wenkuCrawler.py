# -*- coding: utf-8 -*-
'''
程序功能：爬取文库的文档，以图片的形式保存。

效果：以这种方式处理后的图片貌似清晰度有点差

Tips: 将下载的图片全选右键可选择打印成PDF。
'''
import requests
from bs4 import BeautifulSoup
import os

def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""

folderName='所有图片'
if not os.path.exists(folderName):
    os.mkdir(folderName)     
    
    
'''最大页面数以及URL 需要自己手动指定'''
maxPageNum=43

basicUrl='https://wapwenku.baidu.com/view/6d0d432758fb770bf78a5542.html?pn={page}&pu='
''' '''

for page in range(1,maxPageNum+1):
    html = getHTMLText(basicUrl.format(page=page))
    soup = BeautifulSoup(html, "html.parser").find('div',attrs={'class':'content bgcolor1'})
    
    pictureLink=soup.find('a').get("href")
    filename=folderName+'/'+str(page)+'.jpg'
    with open(filename, 'wb') as f:
            file=requests.get(pictureLink)
            f.write(file.content)#保存文件用二进制形式
    print('save file: '+filename)