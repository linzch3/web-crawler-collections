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

爬取[深圳市政府在线网站][深圳市政府在线网站]的在线咨询投诉公开问题的相关信息

[深圳市政府在线网站]:http://www.sz.gov.cn/cn/hdjl/zxts/dfyjcx/




