"""功能:通过爬虫快速获取数据图片"""

import os
import sys
import time
import urllib
import requests
import re
from bs4 import BeautifulSoup
import time

header = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'     # 伪装浏览器
}
url = "https://cn.bing.com/images/async?q={0}&first={1}&count={2}&scenario=ImageBasicHover&datsrc=N_I&layout=ColumnBased&mmasync=1&dgState=c*9_y*2226s2180s2072s2043s2292s2295s2079s2203s2094_i*71_w*198&IG=0D6AD6CBAF43430EA716510A4754C951&SFX={3}&iid=images.5599"   # 搜索关键字

save_path = '../shaYv'

DE_WEIGHT = False    # 是否去重


def getImage(url, count):    # 获取图片
    '''从原图url中将原图保存到本地'''
    try:    # 有些图片无法打开，所以要用try
        num = 1                                  # 图片编号
        datafiles = os.listdir(save_path)        # 获取文件夹中的文件名
        if DE_WEIGHT:                            # 去重
            img_name = str(num) + '.jpg'         # 图片名
            while img_name in datafiles:         # 如果图片名已存在
                num += 1                         # 图片编号加1
                img_name = str(num) + '.jpg'  #
        else:                                 # 不去重
            img_name = str(count) + '.jpg'    # 图片名
        time.sleep(0.5)                       # 睡眠0.5秒，防止被封
        urllib.request.urlretrieve(url, os.path.join(save_path, img_name))    # 保存图片
    except Exception as e:                                                    # 如果图片无法打开
        time.sleep(1)                                                         # 睡眠1秒，防止被封
        print("本张图片获取异常，跳过...")                                        # 打印异常信息
    else:
        print("图片+1,成功保存 " + str(count + 1) + " 张图")                     # 打印成功信息


def findImgUrlFromHtml(html, rule, url, key, first, loadNum, sfx, count):                   # 从缩略图列表页中获取原图url
    '''从缩略图列表页中找到原图的url，并返回这一页的图片数量'''
    soup = BeautifulSoup(html, "html.parser")                                                   # 解析html
    link_list = soup.find_all("a", class_="iusc")                                                   # 找到所有的a标签
    url = []
    for link in link_list:                                                                          # 遍历a标签
        result = re.search(rule, str(link))
        # 将字符串"amp;"删除
        url = result.group(0)
        # 组装完整url
        url = url[8:len(url)]
        # 打开高清图片网址
        getImage(url, count)
        count += 1
    # 完成一页，继续加载下一页
    return count


def getStartHtml(url, key, first, loadNum, sfx):
    '''获取缩略图列表页'''
    page = urllib.request.Request(url.format(key, first, loadNum, sfx),
                                  headers=header)
    html = urllib.request.urlopen(page)
    return html


if __name__ == '__main__':
    name = "鲨鱼"    # 图片关键词
    countNum = 2000  # 爬取数量
    key = urllib.parse.quote(name)
    first = 1
    loadNum = 35    # 每页加载数量
    sfx = 1         # 页数
    count = 0           # 计数器
    rule = re.compile(r"\"murl\"\:\"http\S[^\"]+")          # 匹配原图url的正则表达式
    if not os.path.exists(save_path):                           # 如果文件夹不存在
        os.makedirs(save_path)                               # 创建文件夹
    while count < countNum:
        html = getStartHtml(url, key, first, loadNum, sfx)
        count = findImgUrlFromHtml(html, rule, url, key, first, loadNum, sfx,
                                   count)
        first = count + 1
        sfx += 1



