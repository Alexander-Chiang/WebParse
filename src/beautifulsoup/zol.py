'''
Created on 2016-12-12

@author: Sawatari
'''

from bs4 import BeautifulSoup
import requests
import time

urls = ['http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_0_99_2_0_{}.html'.format(str(i)) for i in range(1, 10)]

def get_notebook(url, data=None):
    info = []
    wb_data = requests.get(url)
    time.sleep(3)
    Soup = BeautifulSoup(wb_data.text, 'lxml')
    names = Soup.select(
        '#J_PicMode > li > h3 > a')
    images = Soup.select(
        '#J_PicMode > li > a > img')
    prices = Soup.select(
        '#J_PicMode > li > div.price-row > span.price.price-normal > b.price-type')
    favors = Soup.select(
        '#J_PicMode > li > div.comment-row > span > em')

    for name, image, price, favor in zip(names, images, prices, favors):
        temp = favor.get('style')
        fav = temp.split(':')[1]
        data = {
            'name': name.get_text(),
            'image': image.get('.src'),
            'price': price.get_text(),
            'favor': fav
        }
        info.append(data)

# sifting
    for i in info:
        score = i['favor'].split('%')[0]
        if float(score) > 85:
            print(i['name'], '价格：' + i['price'], '好评率：' + i['favor'], '图片：' + i['image'])

for single_url in urls:
    get_notebook(single_url)

