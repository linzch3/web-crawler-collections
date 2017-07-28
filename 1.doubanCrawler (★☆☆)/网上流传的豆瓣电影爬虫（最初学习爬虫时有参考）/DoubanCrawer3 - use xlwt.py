# -*- coding:utf-8 -*-
'''
使用xlwt处理excel文件版本
注意！！！要在python3的环境下运行才不会报错
'''
import requests, re
from bs4 import BeautifulSoup
from xlwt import *

wb = Workbook()
ws1 = wb.add_sheet('movietop250')
ws1.col(0).width,ws1.col(1).width,ws1.col(2).width,ws1.col(3).width=10000,4000,4000,50000#3000约为一格的长度

dest_filename = 'movie.xls'
DOWNLOAD_URL = 'http://movie.douban.com/top250/'


def download_page(url):
    """获取url地址页面内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data


def parse_html(doc):
    soup = BeautifulSoup(doc, 'html.parser')#生成实例
    ol = soup.find('ol', class_='grid_view')#调用实例
    name = []  # 名字
    star_con = []  # 评价人数
    score = []  # 评分
    info_list = []  # 短评
    for i in ol.find_all('li'):
        detail = i.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).get_text()  # 电影名字
        level_star = i.find('span', attrs={'class': 'rating_num'}).get_text()  # 评分
        star = i.find('div', attrs={'class': 'star'})
        star_num = re.findall(r'\d+',str(star))[-1]#评价人数

        info = i.find('span', attrs={'class': 'inq'})  # 短评
        if info:  # 判断是否有短评
            info_list.append(info.get_text())
        else:
            info_list.append('无')
        score.append(level_star)

        name.append(movie_name)
        star_con.append(star_num)
    page = soup.find('span', attrs={'class': 'next'}).find('a')  # 获取下一页
    if page:
        return name, star_con, score, info_list, DOWNLOAD_URL + page['href']
    return name, star_con, score, info_list, None


def main():
    url = DOWNLOAD_URL
    name = []
    star_con = []
    score = []
    info = []
    while url:
        doc = download_page(url)
        movie, star, level_num, info_list, url = parse_html(doc)
        name = name + movie
        star_con = star_con + star
        score = score + level_num
        info = info + info_list
    for (i, m, o, p) in zip(name, star_con, score, info):
        ws1.write(name.index(i), 0, i)
        ws1.write(name.index(i), 1, m)
        ws1.write(name.index(i), 2, o)
        ws1.write(name.index(i), 3, p)
    wb.save(dest_filename)


if __name__ == '__main__':
    main()
