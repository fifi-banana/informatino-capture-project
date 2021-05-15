# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 17:47:18 2020
将关键字单独复制出来，粘贴在txt里面

@author: Lenovo
"""

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba

filename = "key.txt"
with open(filename) as f:
    text = f.read()

#%%%%%
# 中文的话分词
# text = ','.joint(jieba.cut(keyword))
word = WordCloud(width=5000, height=5000,scale=2, mode='RGBA', background_color=None).generate(text)

#%%%%
# %pylab inline
import matplotlib.pyplot as plt
plt.imshow(word,interpolation='bilinear')
plt.axis("off")