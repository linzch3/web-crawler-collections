# WebCrawler_Collection
--------------------------------------
### 1.[doubanCrawler][1] (★☆☆)
爬取豆瓣TOP250电影的评分、评价人数、短评等信息，并在其保存在txt文件中。

[1]:http://blog.csdn.net/linzch3/article/details/62444947

### 2.[Ip address automatic query][2] (★☆☆)
实现用户输入IP地址，利用爬虫程序为其查询IP地址的地理位置的功能。

[2]:http://blog.csdn.net/linzch3/article/details/62273278

### 3.[pdfBatchDownloader][3] (☆☆☆)
批量下载开放服务器的pdf文件。

[3]:http://blog.csdn.net/linzch3/article/details/68948802

### 4.GovernmentAffairsCrawler (★★☆)
爬取[广东省广东省人民政府首页][广东省广东省人民政府首页]的政务公开新闻对应的链接、标题、发布日期、正文。

[广东省广东省人民政府首页]:http://www.gd.gov.cn/govpub/xxts/index.htm

### 5.WeiboCommentsCrawler (★★★)
该爬虫分为3种：

1.通过id抓取评论信息的WeiboCommentsCrawlerByIds和抓取转发信息的WeiboRepostCommentsCrawlerByIds

微博上每一条首发的微博都有特定的id，通过指定id，爬取特定单条微博被转后发用户附上的评论以及对应微博下的评论，通过jieba进行分词并用wordcloud绘制对应的词云。

其中指定id的方法就是：将id添加到与代码在同目录下的weiboIds.csv文件中

2.WeiboCommentsCrawlerByKeywords

对关键词搜索出来的页面进行数据抓取

### 6.szgovCrawler (★★★)

爬取[深圳市政府在线网站][深圳市政府在线网站]的在线咨询投诉公开问题的相关信息，完成如下的几个任务：

---绘制 前30个咨询数量最高的部门和所有部门（整合在一起） 的问题咨询数量的年份、月份、一周的变化图

---使用SnowNLP为文本数据添加情感值的分析

----绘制 前30个咨询数量最高的部门和所有部门（整合在一起） 的词云（分词文件可不断完善以提高分词效果）

[深圳市政府在线网站]:http://www.sz.gov.cn/cn/hdjl/zxts/dfyjcx/

### 7.zhgovCrawler (★★☆)

爬取[珠海市政府网页][珠海市政府网页]中关于投诉以及咨询的内容

具体包含：主题、日期、投诉/咨询人、处理单位、处理状态、受理意见

[珠海市政府网页]:http://www.zhuhai.gov.cn/hd/zxts_44606/tsfk/

### 8.wenkuCrawler(☆☆☆)

爬取百度文库文章（后台以图片形式储存的一种）对应的图片

### 9.zsgovCrawler(★☆☆)
爬取[中山市政府市长信箱][中山市政府市长信箱] 中的所有数据

具体包含：诉求编号、所属部门、诉求类型、处理状态、诉求标题、递交时间、诉求来源、事发地点、诉求内容、回复意见

[中山市政府市长信箱]: http://www.zs.gov.cn/main/zmhd/

### 10.hzgovCrawler(★☆☆) 
爬取[惠州市人民政府网页][惠州市人民政府网页]中关于网络问政的内容

具体包含：来信人、来信主题、受文单位、来信时间、来信类型、办理状态、来信内容、最终回文单位、最终办理时间、最终处理结果 共10项数据

[惠州市人民政府网页]:http://www.huizhou.gov.cn/wlwzlist.shtml?method=letters4bsznList3&pager.offset=0
