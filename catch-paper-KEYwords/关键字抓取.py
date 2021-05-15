# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 16:27:11 2020

关键字文献对应的关键字抓取，用于延伸领域相关性

尝试建立词云和知识图谱

@author: fifibanana
"""
import requests
from lxml import etree
import pandas as pd
import os
import math
from requests.packages import urllib3

# keyWord = input("Please input the key words that you want to search: ")
# performance based seismic design reinforced concrete

def key_word():
    # 将输入的关键字分解，构造搜索的url
    # 要用到字符串的分解和拼接
    key_words = input("Please input the key words that you want to search: ")
    key_group = key_words.split(' ')
    
    return key_group

def create_url(key_group):
    
    # 根据分开的关键词创建一个新的url
    base_url = 'https://www.sciencedirect.com/search?qs=' + key_group[0]
    
    # range函数始终不会索引到最后一个数字的
    for i in range(1,len(key_group)):
        base_url = base_url +'%20' + key_group[i]
    print(base_url)
    return base_url

def get_html(url):
    # 爬取之前要先获取html信息，以便解析
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    
    try:
        html = requests.get(url,headers = headers)
        html.encoding = html.apparent_encoding
        if html.status_code == 200:
            # print("成功获取网页")
            pass
    except Exception as e:
        print("获取源代码失败：%s" % e)
        
    return html.text


def get_paper_url(html):
    # 得到本页里每一个论文的链接
    paper_url = []
    html = etree.HTML(html)
    lis = html.xpath("//*[@id='main_content']/main/div[1]/div[2]/div[2]/ol/li")
    # print(len(lis))
    
    # lis = lis[0:5]
    
    for li in lis:
        # 因为含有其余的选项不属于文献，所以要用try命令
        try:
            link = li.xpath(".//div/div/h2/span/a/@href")[0]
            link = link.split('pii')
            link = link[0]+"abs/pii"+link[1]
            link = "https://www.sciencedirect.com" + link
            paper_url.append(link)
        except:
            pass
    # print(paper_url)
    print(len(paper_url))
    return paper_url
 
# def new_html()    

def parse_html(paper_url):
    key_infos = []
    #根据得到的每个文献的url列表，逐个循环得到所得信息
    for url in paper_url:
        # 新链接的打开方式
        # new_url = "https://www.sciencedirect.com" + url
        html2 = get_html(url)
        
        html = etree.HTML(html2)
        # 进入论文页面后
        name = html.xpath("//*[@id='screen-reader-main-title']/span/text()")[0]
        try:
            pub_year = html.xpath("//*[@id='publication']/div[2]/div/text()")[0]
            year = pub_year.split(',')
            try:
                year = year[1].strip()
            except:
                year = pub_year
        except:
            year = "NONE"
        
        author_1st = html.xpath("//*[@id='author-group']/a[1]/span/span[1]/text()")[0]
        # 可能没有第二作者
        try:
            author_2nd = html.xpath("//*[@id='author-group']/a[2]/span/span[1]/text()")[0]
        except:
            author_2nd = "NONE"
        
        try:
            magazine = html.xpath("//*[@id='publication-title']/a/text()")[0]
        except:
            magazine = html.xpath("//*[@id='publication']/div[1]/a/h2/text()")[0]
        
        # 关键字信息，可能会有多个，用;作分隔符方便分开
        # 先得到关键字的总和
        all_key_word = html.xpath("//div/div[@class='keyword']")
        # 要用个循环才能返回值
        key_words = []
        for i in all_key_word:
            word = i.xpath(".//span/text()")[0]
            key_words.append(word)
            
        # //*[@id="mathjax-container"]/div[2]/article/div[6]/div[1]/div[1]/span/text()
        # print(key_words)
        
        key_info = {'name':name,'pub_year':year,'author_1st':author_1st,
                    'author_2nd':author_2nd,'magazine':magazine,'key_words':key_words}
        # print(key_info)
    
        key_infos.append(key_info)
        # print(name)
        print('.',end = '')
        # 当进度条
    return key_infos

def how_many_pages(html):
    html = etree.HTML(html)
    num_results = html.xpath("//*[@id='srp-facets']/div[1]/h1/span/text()[1]")[0]
    # 字符串转化为数字
    # 要进行两步分解
    num_results = str(num_results)
    num_results = num_results.split(' ')[0].split(',')
    num_results = num_results[0] + num_results[1]
    num_results = int(num_results)
    num_pages = math.ceil(num_results / 25)
    print("The total pages is %s :" %num_pages)
    return num_pages

if __name__ == '__main__':
    
    
    # base_url根据自己输入得出
    # base_url = 'https://www.sciencedirect.com/search?qs=performance%20based%20seismic%20design'
    key_group = key_word()
    base_url = create_url(key_group)
        
    html1 = get_html(base_url)
    
    # 首先识别有多少页，自行选择要爬取多少页
    pages = how_many_pages(html1)
    # 但是好像界面里面最多也就240页
    
    num_searching_pages = input("Input the num of pages that you want: ")
    num_searching_pages = int(num_searching_pages)
    PAPER_INFO = []
    
    for i in range(num_searching_pages):
        
        # paper_url = []
        # 用来收集每篇文献的url，省的用点击的命令
        # 先获得此页的base_url
        each_base_url = base_url + '&offset=' + str(i*25)
        print(each_base_url)
        html = get_html(each_base_url)
        paper_url = get_paper_url(html)
        
        # 新的链接方式：https://www.sciencedirect.com  /science/article/abs/pii/S0267726118303695
        # 其中后半部分已经爬出，加上前半截即可
        # 得到了整页的url，循环每个url，分别爬取题目、作者、年份、关键字信息
        # paper_url1 = paper_url[0:4]
                    
        paper_info = parse_html(paper_url)
        
        PAPER_INFO.extend(paper_info)
        print("The %s page is collected!" % (i+1))
    
    data = pd.DataFrame(PAPER_INFO)
    data.to_csv('RC structure seismic vulnerability assessment.csv')
    
    print("成功获取文献信息")
    # for i in range(10):
    #     # https://www.sciencedirect.com/search?qs=performance%20based%20seismic%20design&offset=25
    #     url = base_url + '&offset=' + str(i*25)

