# coding=utf-8
import csv

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import PIL
from wordcloud import WordCloud

# 設定雲形狀
linxi_mask = np.array(PIL.Image.open('linxi.png'))

text = open('lyrics_assemble_final.csv')

cloud_text = ' '.join(text)

# 停用詞
stopwords = set()
with open('stop_words.csv', newline='') as f:
    rows = csv.reader(f)
    for row in rows:
        stopwords.add(''.join(row))

wc = WordCloud(background_color="white",
               max_words=2000,
               mask=linxi_mask,
               stopwords=stopwords,
               contour_width=3,  # 設定輪廓寬度
               contour_color='steelblue',  # 設定輪廓顏色
               font_path='/Users/huangyiling/Github/lyrics_nlp_LinXi_AlbertLeung/venv/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf/TaipeiSansTCBeta-Bold.ttf')


my_font = fm.FontProperties(
    fname='/Users/huangyiling/Github/lyrics_nlp_LinXi_AlbertLeung/venv/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf/TaipeiSansTCBeta-Bold.ttf')

# 從文字生成wordcloud
wc.generate(cloud_text)

# 儲存到檔案
wc.to_file("worldcloud_counts.png")

# 顯示圖片
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()  # 新建一個圖片，把mask也顯示出來
plt.imshow(linxi_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
plt.show()
