# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 10:17:09 2020

@author: fifibanana
"""


import requests
from lxml import etree
import pandas as pd
import os
import selenium
from requests.packages import urllib3

# 验证选项：
# Type:	Rectangular
# Test Configuration:	Cantilever
# Failure Type:	Flexure
# url = 'https://nisee.berkeley.edu/spd/servlet/display?format=html&id=' + str(i)


def get_html(url):
    
    ## 开发者工具 network 找header
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    try:
        html = requests.get(url,verify = False)
        # html = requests.get(url,hearders = headers)
        #html = requests.post(url, headers={"Connection": "close"})
        #requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
        urllib3.disable_warnings()
        html.encoding = html.apparent_encoding
        # if html.status_code == 200:
            # print("成功获取源代码")
            # print(html.text)
    except Exception as e :
        print("获取源代码失败：%s" % e)
        
    return html.text

# Error_Group = []
# OK_Group = []
    
# def is_needed_group(i,html):
    
#     global Error_Group
#     global OK_Group
#     # 先判断类别是否符合
#     # 验证选项：
#     # Type:	Rectangular
#     # Test Configuration:	Cantilever
#     # Failure Type:	Flexure
#     # 1/抓取截面形状
#     type_shape = html.xpath(".//tr[3]/td[2]/text()")[0]
#     # print(type_shape)
    
#     Configuration = html.xpath(".//tr[13]/td[2]/text()")[0]
#     # print(Configuration)
    
#     try:
#         Failure_type = html.xpath(".//tr[34]/td[2]/text()")[0]
#     except:
#         Failure_type = html.xpath(".//tr[35]/td[2]/text()")[0]
#         # print("%s is no ok" % i)
#         # Error_Group.append(i)
#         # clarify = 0
#         # return clarify
#     # print(Failure_type)
    
#     clarify = ((type_shape == 'Rectangular')& (Configuration =='Cantilever')&(Failure_type =='Flexure')&\
#                (Failure_type == 'Flexure'))
#     # clarify2 = 
#     if clarify:
#         print("Group%s is the needed group" % i)
#         OK_Group.append(i)
#     else:
#         print("Group%s is NOT the needed group" % i)
#         Error_Group.append(i)
        
#     return clarify
    
#     # 可用的id名已经保存
#     # 这个函数不需要调用了，完善一点可以做个分类器，类似search功能
   
    
    
    
def parse_html(html):
    
    ref_name = html.xpath('.//tr[2]/td[2]/text()')[0]
    print(ref_name)
    
    # 材料
    concrete_strength = html.xpath('.//tr[7]/td[2]/text()')[0]
    
    Transverse_yield_max = html.xpath('.//tr[8]/td[2]/text()')[1]
    # print(Transverse_yield_max)
    
    Longitudinal_yield_max_cor = html.xpath('.//tr[9]/td[2]/text()')[1]
    try:
        Longitudinal_yield_max_inter = html.xpath('.//tr[9]/td[2]/text()')[2]
    except:
        Longitudinal_yield_max_inter = "None"
    
    # 几何
    section = html.xpath('.//tr[11]/td[2]/text()')[0]
    length =  html.xpath('.//tr[12]/td[2]/text()')[0]
    # print(section)
    # load
    load = html.xpath('.//tr[15]/td[2]/text()')[0]
    
    # 纵筋直径 数量 配筋率
    diameter = html.xpath('.//tr[20]/td[2]/text()')[0]
    num_bar = html.xpath('.//tr[21]/td[2]/text()')[0]
    cover = html.xpath('.//tr[22]/td[2]/text()')[0]
    reinforce_ratio = html.xpath('.//tr[24]/td[2]/text()')[0]
    
    # 箍筋样式、肢数、直径&间距、配箍率
    tran_type = html.xpath('.//tr[26]/td[2]/text()')[0]
    num_tran = html.xpath('.//tr[27]/td[2]/text()')[0]
    close_spacing = html.xpath('.//tr[28]/td[2]/text()')[0]
    
    # 多出来的一个是加密区和非加密区的间隔   部分数据是没有非加密区的间隔的
    # 所以如果有非加密区数据的，后面的行数需要自行加1
    
    check_wide_space_exist = html.xpath('.//tr[29]/td[1]/text()')[0]
    # print(check_wide_space_exist)
    check = (check_wide_space_exist == 'Region of Wide Spacing:')
    
    if check:
        # 配箍率
        tran_ratio = html.xpath('.//tr[30]/td[2]/text()')[0]
        # print(tran_ratio)
        # 剪跨和轴压比
        span_to_depth_ratio = html.xpath('.//tr[32]/td[2]/text()')[0]
        axial_load_ratio = html.xpath('.//tr[33]/td[2]/text()')[0]
    else:
        # 配箍率
        tran_ratio = html.xpath('.//tr[29]/td[2]/text()')[0]
        # print(tran_ratio)
        # 剪跨比和轴压比
        span_to_depth_ratio = html.xpath('.//tr[31]/td[2]/text()')[0]
        axial_load_ratio = html.xpath('.//tr[32]/td[2]/text()')[0] 
        
        
    # 保存成字典形式返回  共18个
    column_info = {'ref_name':ref_name,'concrete_strength':concrete_strength,\
                   'Transverse_yield_max':Transverse_yield_max,'Longitudinal_yield_max_cor':Longitudinal_yield_max_cor,\
                       'Longitudinal_yield_max_inter':Longitudinal_yield_max_inter,\
                           'section':section,'length':length,'load':load,'diameter':diameter,\
                               'num_bar':num_bar,'cover':cover,'reinforce_ratio':reinforce_ratio,\
                                   'tran_type':tran_type,'num_tran':num_tran,'close_spacing':close_spacing,\
                                       'tran_ratio':tran_ratio,'span_to_depth_ratio':span_to_depth_ratio,\
                                           'axial_load_ratio':axial_load_ratio}
    
    
    return column_info

def get_txturl(html):
    # 获得下载txt的url
    try:
        txturl = html.xpath('.//tr[36]/td[2]/a/@href')[0]
    except:
        txturl = html.xpath('.//tr[37]/td[2]/a/@href')[0]
    
    # txturl = txt.get_attribute("href")
    # print(txturl)
    
    return txturl
    
def downloadtxt(i,url):
    
    exper_txt = requests.get(url).content
    num_data = str(i)
    
    with open(num_data + '.txt','wb') as f:
        print("正在下载：%s" % url)
        
        f.write(exper_txt)



if __name__ == '__main__':
    
    flexure_group = pd.read_csv('ok_id.csv')
    
    ID = flexure_group.ok_id
    print(len(ID))
    
    COLUMN_INFO = []
    COLUMN_DATAS = []
    
    
    # 根据url获取HTML信息
    for i in ID :
        url = 'https://nisee.berkeley.edu/spd/servlet/display?format=html&id=' + str(i)
    
        html_un = get_html(url)
        # 解析HTML的过程才能判断是否是想要的柱子类型
        # 解析命令，都在html只是str格式
        html = etree.HTML(html_un)
        
        # 判断是否想要的组
        # clarify = is_needed_group(i,html)
        
        # if clarify:
        #     column_datas = parse_html(html)
        # (okfile.ok_id[0:10])调用可用的id
        
        column_info = parse_html(html)
        #试验数据
        column_datas = get_txturl(html)
        
        COLUMN_INFO.append(column_info)
        COLUMN_DATAS.append(column_datas)
        
    # 下载txt文件
    os.mkdir('datafile')
    os.chdir(r'D:\fifi_code\peer_flexualColumn\datafile')
    
    for i in range(len(ID)):
        downloadtxt(i,COLUMN_DATAS[i])
    
    os.chdir(r'D:\fifi_code\peer_flexualColumn')
    
    column_information = pd.DataFrame(COLUMN_INFO)
    column_information.to_csv('column_information.csv')
    
    print("信息保存到本地")
        
        
        
        
        