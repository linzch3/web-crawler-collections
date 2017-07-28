#-*- coding:utf-8 -*-
import requests
import re
import os
basicUrl='http://public.dhe.ibm.com/software/analytics/spss/documentation/modeler/14.2/zh_CN/'

def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""

html = getHTMLText(basicUrl)
r= re.compile(r'\w*.pdf')
for filename in r.findall(html):#找到网页上的pdf文件
    if not os.path.exists(filename):#若该文件之前没有保存过，则保存下来
        with open(filename, 'wb') as f:
            file=requests.get(basicUrl+filename)
            f.write(file.content)#保存文件用二进制形式

