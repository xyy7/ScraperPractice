import json
import re
# 2. 
from urllib.request import Request, urlopen

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 1. 简单添加header，网络连接都不行
# import requests
# def get_html(url):
#     try:
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
#         response = requests.get(url, headers)
#         return response.text.encode(response.encoding).decode()
#     except requests.RequestException as e:
#         print(e)
#         return None

# 2. urllib简单添加header，可以获取一点点没有价值的html
# def get_html(url):
#     try:
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
#         response = Request(url, headers=headers)
#         html = urlopen(response).read()  # 添加headers，解决某些网站的反爬虫
#         return html.decode()
#     except:
#         return None


# 3. selenium模拟，但是直接获取，还是获取不到
def get_html(url):
    browser = webdriver.Chrome()
    browser.get(url)
    WAIT = WebDriverWait(browser, 10)
    html = browser.page_source
    return html


def main():
    url = 'https://www.instagram.com/brinacocker/#'
    html = get_html(url)  # 请求==》html页面
    print(html)
    with open('tmp.txt',encoding='utf8',mode='w') as file:
        file.write(html)
 


if __name__ == "__main__":
    main()
