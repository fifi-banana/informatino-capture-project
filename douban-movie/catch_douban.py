# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:43:27 2020

@author: Lenovo
"""

import requests
from lxml import etree
import pandas as pd
import os
# 建立文件夹需要用到OS库

def get_html(self):
    
    # 字典类型，要补充引号
    # 在网页中的开发者工具中寻找header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    
    try:
        html = requests.get(url,headers = headers)
        html.encoding = html.apparent_encoding
        if html.status_code == 200:
            #200代表服务器正常响应， 404代表页面未找到
            print("成功获取源代码")
            # print(html.text)
    except Exception as e :
        print("获取源代码失败:%s" % e)
    
    return html.text
            
def parse_html(html):
    
    
    movies = []
    imgurls = []
    html = etree.HTML(html)
    lis = html.xpath("//ol[@class='grid_view']/li")
    print(len(lis))
    
    # xpath 返回的是一个列表
    for li in lis:
        # name标签在span标签下，span标签的class是title
        # 电影名
        name = li.xpath(".//a/span[@class='title']/text()")[0] ;#抓取title下的文本,把列表中的元组取出
        # 一定要写. 表明是从这个节点开始的
        print(name)
        
        # 导演和演员 以及影片类别
        director_actor = li.xpath(".//div[@class='bd']/p/text()")[0].strip()
        info = li.xpath(".//div[@class='bd']/p/text()")[1].strip()
        # strip去空格
        
        # 评分人数和评分
        rating_score = li.xpath(".//div[@class='star']/span[2]/text()")[0]
        rating_num = li.xpath(".//div[@class='star']/span[4]/text()")[0]
        
        # 简介 恰好碰到九品芝麻官没有简介，所以要设置跳过
        try:
            
            introduce = li.xpath(".//p[@class='quote']/span/text()")[0]
        except:
            introduce = "None"
        
        ## 抓取海报
        imgurl = li.xpath(".//img/@src")[0]
        
        # 保存成字典形式
        movie = {'name':name,'director_actor':director_actor,'info':info,\
                 'rating_score':rating_score,'rating_num':rating_num,\
                 'introduce':introduce}
        
        # 把movie添加进movies列表
        movies.append(movie)
        imgurls.append(imgurl)
        
    return movies,imgurls
        
    # print(introduce)

def downloadimg(url,movies):
    
    if 'movieposter' in os.listdir(r'D:\fifi_code\网页爬取'):
        pass
    else:
        os.mkdir('movieposter')
    os.chdir(r'D:\fifi_code\网页爬取\movieposter')
    # 移动路径到该文件夹内
    
    img = requests.get(url).content
    
    with open(movies['name'] + '.jpg','wb') as f:
        print("正在下载：%s" % url)
        
        #wb是一种open的模式：以二进制格式打开一个文件只用于写入。
        #如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。
        #如果该文件不存在，创建新文件。一般用于非文本文件如图片等。
        f.write(img)
        # 将数据写入文件

if __name__ == '__main__':
    #if __name__ == '__main__':作用:
    #python文件通常有两种使用方法，第一是作为脚本直接执行，第二是 import 到其他的 python 脚本中被调用（模块重用）执行
    # 直接执行本文件的话，语句前后的命令都能执行
    # 如果import这个文件，之前的语句被执行，之后的没有被执行
    
    # 进行十页的循环抓取
    MOVIES = []
    IMGURLS = []
    
    for i in range(10):
        
        url = 'https://movie.douban.com/top250?start=' + str(i*25) + '&filter='
        
        html = get_html(url)
    
        # 获取了之后，开始解析
        movies = parse_html(html)[0]
        imgurls = parse_html(html)[1]
        
        MOVIES.extend(movies)
        IMGURLS.extend(imgurls)
        # extend() 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
    
    for i in range(250):
        downloadimg(IMGURLS[i],MOVIES[i])
        # 此时可以直接索引第几行，但是用到pandas的时候就有变化
    
    # 要把路径移回来保存文件
    
    os.chdir(r'D:\fifi_code\网页爬取')
    moviedata = pd.DataFrame(MOVIES)
        
    # print(moviedata)
    
    # print(moviedata.introduce[0:3])
    
    # print(moviedata.loc[1])
    
    # moviedata.to_csv('movie.csv')
    moviedata.to_excel('movie.xlsx')
    
    print("电影信息保存到本地")
