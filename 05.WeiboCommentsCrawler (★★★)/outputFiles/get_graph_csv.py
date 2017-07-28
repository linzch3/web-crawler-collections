# -*- coding: utf-8 -*-
'''
程序功能：得到 用于gephi绘图的csv文件

该文件有2列：Source,Target，编码方式选择GBK格式

'''
import pandas
import re
names=['comments','date','user_id','user_name','user_profile_image_url']

topics=['八达岭老虎咬人案','女子痛斥医院票贩','西安地铁三号线']
#topics=['八达岭老虎咬人案']
for topic in topics:
    idpath="./"+topic+"/id.csv"
    ids=pandas.read_csv(idpath).id
    for id in ids:
        datapath="./{topic}/id{id}-RepostComment.csv".format(topic=topic,id=id)
        df=pandas.read_csv(datapath,names=names,encoding='GBK')
        
        pattern=re.compile(r"//@.*?:")
        
        Source=[]
        Target=[]
        for comments,user_name in zip(df.comments,df.user_name):
            results=re.findall(pattern,comments)
            
            if len(results)>0:
                Source.append(results[0][3:-1])
            else:
                 Source.append("发布微博的博主")
                
            Target.append(user_name)
                
                
        contentDF = pandas.DataFrame({
        'Source':Source,
        'Target':Target,
        })    
        result_path="./{topic}/id{id}-RepostComment-SourceTarget.csv".format(topic=topic,id=id)
        contentDF.to_csv(result_path,mode='w', header=True,index=False)
        print("save file: "+result_path)
                