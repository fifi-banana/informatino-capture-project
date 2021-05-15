# -*- coding: utf-8 -*-
# -*- coding: cp936 -*-
"""
Created on Mon Jul 13 09:58:38 2020

制作中尉词云

@author: Lenovo
"""


from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
import matplotlib.pyplot as plt

filename = "Chinese.txt"

text = open('Chinese.txt','rb').read()



# 设置fontpath
font = r'C:\Windows\Fonts\SIMHEI.TTF'

text = ''.join(jieba.cut(text))
# text = str(text)
word = WordCloud(font_path=font,width=800,height=600,mode='RGBA',background_color=None).generate(text)

plt.imshow(word,interpolation='bilinear')
plt.axis('off')
