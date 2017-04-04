# -*- coding: utf-8 -*-
import os
import urllib
import pandas

keyword = '中山大学'
data = pandas.read_csv(
    "outputFiles/weibo_search_%s.csv" % (keyword)
)

directory = "outputFiles/%s" % (keyword);
if not os.path.exists(directory):
    os.makedirs(directory)

data = data.dropna()

import urllib.request
opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')

for index, row in data.iterrows():
    wId = row['id']
    imageURL = row['pics']
    localFile = "%s\\%s.png" % (directory, wId);
    try:
        filename, headers = opener.retrieve(imageURL, localFile);
    except Exception as e:
        print(str(e))
        