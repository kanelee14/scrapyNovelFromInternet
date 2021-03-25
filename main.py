# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 16:30
# @Author  : Mat
# @File    : main.py
# @Software: PyCharm

import sys

import requests
from tqdm import tqdm
import time
from bs4 import BeautifulSoup

# 获取网页的html
def getHtml(url):
    url = url
    res = requests.get(url)
    res.encoding = 'utf-8'
    html = res.text
    # print(html)
    return html

# 解析小说章节页面,获取所有章节的子链接
def jsoupUrl(html):

    # 获取soup对象
    url_xiaoshuo = BeautifulSoup(html)
    # 因为我们要拿取class为box_con中的div
    class_dict = {'class': 'box_con'}
    chapters = url_xiaoshuo.find_all('div', attrs=class_dict)
    # print(chapters)
    # 因为分析html中的代码可以发现div的class为box_con的有两个,通过上面的代码返回的是一个list格式的结果，所以下面的索引应该是１
    # 我们要获取dd中的值，所以find_all，这个方法返回的是一个list集合
    chapters = chapters[1].find_all('dd')
    return chapters

# 解析小说每个章节的的主要内容
def getContent(target):
    req = requests.get(url = target)
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    texts = bf.find('div', id = 'content')
    content = texts.text.strip().split('\xa0'*4)
    return content


if __name__ == '__main__':

    time.sleep(20)
    # 小说网地址 sys.argv需要terminal运行，
    # IDE 会报sys.argv[1] IndexError: list index out of range
    # serverUrl = 'https://www.vbiquge.com'
    serverUrl = sys.argv[1]

    #某一个小说目录链接
    # reqUrl = getHtml("https://www.vbiquge.com/84_84063/")
    reqUrl = getHtml(sys.argv[2])

    # 小说名字
    # book_name = 'novelDemo.txt'
    book_name = sys.argv[3]


    chapters = jsoupUrl(reqUrl)
    for chapter in tqdm(chapters):
        chapter_name = chapter.string
        url = serverUrl + chapter.a['href']
        # print(url)

        content = getContent(url)
        with open(book_name, 'a', encoding='utf-8') as f:
            f.write(chapter_name)
            f.write('\n')
            f.write('\n'.join(content))
            f.write('\n')
    # print(book_name)



