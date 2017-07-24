# -*- coding: utf-8 -*-
'''
demo:
    
爬取肇庆市政府网页（http://wz.zhaoqing.gov.cn/wzpt/index.php?act=political&op=political_list1&curpage=0）中关于网友问政的内容

具体包含：问政标题、 网友名称、问政日期、浏览次数、问政内容、回复内容、牵头部门 共7项数据
'''
import requests
from bs4 import BeautifulSoup
import re
import traceback
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}


def getHTMLText(url,code='utf-8'):
    cnt=0
    while cnt<=100:
        try:
            print("处理URL:"+url)
            r = requests.get(url, timeout=3000)
            r.raise_for_status()
            r.encoding = code
            return r.text
        except:
            cnt=cnt+1
            traceback.print_exc()
            print('\n\n\n\ntry again....\n\n\n\n')
    print('100 times try,but failed........')
    return None
    
basicUrl='http://wz.zhaoqing.gov.cn/wzpt/index.php?act=political&op=political_list1&curpage={page}'
#得到首页的源代码
htmlText=getHTMLText(basicUrl.format(page=0))
#得到页面的子链接(一般用正则表达式来提取更快)
detailPattern=re.compile('political_id=(\d+)')
#得到当前页面下的所有子页面的链接
detailUrls=['http://wz.zhaoqing.gov.cn/wzpt/index.php?act=political&op=political_content&political_id='+ id for id in detailPattern.findall(htmlText)[::2]]

#牵头部门
soup=BeautifulSoup(htmlText, "html.parser")
department=soup.find_all('a',
                          attrs={'style':'color:black;text-align: right'})
牵头部门=[i.getText().strip() for i in department]
print(牵头部门)
'''
下面测试单个链接的抓取
'''
#已回复
testLink1='http://wz.zhaoqing.gov.cn/wzpt/index.php?act=political&op=political_content&political_id=1246360'
#未回复
testLink2='http://wz.zhaoqing.gov.cn/wzpt/index.php?act=political&op=political_content&political_id=1246364'

detailText=getHTMLText(testLink2)
soup1=BeautifulSoup(detailText, "html.parser")
department=soup1.find_all('a',
                          attrs={'style':'color:black;text-align: right'})

questionDetail=soup1.find('div',
                          attrs={'class':'timeline-body-head'})
#问政标题
print(questionDetail.find('h2').getText().strip())
#网友名称
print(questionDetail.find_all('font')[0].getText().strip())
#问政日期
print(questionDetail.find_all('font')[1].getText().strip())
#浏览次数
print(questionDetail.find_all('font')[2].getText().strip())

contentDetail=soup1.find_all('div',
                          attrs={'class':'liuyan_user_text'})
#问政内容
print(contentDetail[0].getText().strip())

#回复内容
if len(contentDetail)==2:
    print(contentDetail[1].getText().strip())
else:
    print('待回复')

'''
下面得到最大页面数
'''

def getMaxPage(basicUrl):
    print('预处理阶段：得到最大页面数')
    test=getHTMLText(basicUrl.format(page=0))
    '''
    使用正则表达式得到 末页 对应的最大页面
    方法：查看源代码->搜素 末页
    注意点：正则表达式要尽量精确，对于匹配最大页面数，使用\d+来匹配相对.*?就比较精确
    '''
    maxPagePattern=r'curpage=(\d+)\"><span>末页</span>'
    return re.findall(maxPagePattern,test)[0]
print(getMaxPage(basicUrl))
