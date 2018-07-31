import requests
from bs4 import BeautifulSoup
import re
import traceback
import os

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}

def getHTMLText(url, code='utf-8'):
    cnt=1
    '''测试版本的getHTMLText函数 只尝试 较少的次数 进行抓取，方便debug'''
    tryTime = 5
    while cnt<=tryTime:
        try:
            #print("处理URL:"+url)
            r = requests.get(url, headers=headers, timeout=3000)
            r.raise_for_status()
            r.encoding = code #r.apparent_encoding
            return r.text
        except:
            cnt=cnt+1
            traceback.print_exc()
            print('\n\ntry again....\n\n')
    print('%s times try, but failed........' % tryTime)
    return None

def printEncoding(url):
    r = requests.get(url, headers=headers, timeout=3000)
    r.raise_for_status()
    print('编码方式为：'+r.apparent_encoding) #注意判断编码方式
    

def createDir(dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        
def fixFileNameOSError(fn):
    fn = fn.replace('\\', '')
    fn = fn.replace('/', '')
    fn = fn.replace(':', '')
    fn = fn.replace('：', '')
    fn = fn.replace('？', '')
    fn = fn.replace('?', '')
    fn = fn.replace('"', '')
    fn = fn.replace('<', '')
    fn = fn.replace('>', '')
    fn = fn.replace('|', '')
    return fn
    
def downloadPDF(fileName, url):
    #加了while循环反而会导致无法中断任务
#     cnt=1
#     tryTime = 5
#     while cnt<=tryTime:
#         try:
            with open(fileName, 'wb') as f:
                file=requests.get(url, verify=False, stream=True)
                f.write(file.content)#保存文件用二进制形式
#         except:
#             cnt=cnt+1
#     print('fail in url: ' + url)    


from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#创建文件夹
rootPath = 'www.emeraldinsight.com'
createDir(rootPath)
# 得到各个volume的链接
year2vol = {2018:[6, 30], 2017:[12,29], 2016:[12, 28],
            2015:[8, 27], 2014:[8, 26], 2013:[7, 25],
            2012:[7, 24], 2011:[7, 23], 2010:[7, 22]}
for year in range(2010, 2019):
    createDir(rootPath + "\\" + str(year))
    for issue in range(1, year2vol[year][0]+1):
        #得到各个issue下面的文献的PDF下载链接以及文献名字
        issueLink = 'https://www.emeraldinsight.com/toc/ijchm/'+str(year2vol[year][1])+'/'+str(issue)
        pdfPattern = re.compile('<a class="ref nowrap" href="(.*?)">(.*?)</a>')
        pdfList = pdfPattern.findall(getHTMLText(issueLink, 'utf-8'))[::2][:-1] #去除冗余无用的链接
        ##通过找到的规律修改链接
        newPdfList = []
        for item in pdfList:
            item = list(item)
            item[0] = 'https://www.emeraldinsight.com' + item[0].replace('full', 'pdfplus')
            item[1] = fixFileNameOSError(item[1])
            newPdfList.append(item)
        #批量爬取PDF
        for item in newPdfList:
            try:
                fileName = ".\\"+ rootPath + "\\" + str(year) + "\\" +item[1]+'.pdf'
                downloadPDF(fileName, item[0])
            except:
                print("year", year, " url:", item[0])
    print(str(year) + "complete....")
