# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2020 Casso.Wong
#      Author:  Casso.Wong
# Start  Date:  2020/05/22
# Last modify:  2020/05/22
#
##############################################################################

from selenium import webdriver   # pip3 install selenium
from bs4 import BeautifulSoup   # pip3 install beautifulsoup4
import json
import sys
import os

# 需要根据谷歌浏览器版本来安装对应的驱动：https://npm.taobao.org/mirrors/chromedriver/    版本 83.0.4103.61（正式版本--不要下载双核版）
# 确认浏览器版本跟driver.exe 版本对应的上就可以
def getHTML(url):
    driver = webdriver.Chrome(r'D:\DonwLoads\chromedriver.exe')  # 这里直接绝对路径启动driver,省事
    driver.get(url)
    return driver.page_source

def parse(html,fname):
    res = BeautifulSoup(html, "html.parser")
    lis = res.find(class_="icon-list").find_all("li")
    for item in lis:
        try:
            icon_class = item.find("i").attrs["class"][0]  # icon 类名字符串
        except:
            continue
        yield {
            "icon_belong":"Element-UI",
            "icon":icon_class
        }
        
def main():
    url = "https://element.eleme.cn/2.12/#/zh-CN/component/icon"
    fname = r"E:\spider\Elementui_icons.json"
    html = getHTML(url)
    data = parse(html,fname)
    with open(fname, "a", encoding="utf-8") as f:
        arr = []
        for item in data:
            arr.append(item)
        f.write(json.dumps(arr, ensure_ascii=False))

if __name__ == "__main__":
    main()
