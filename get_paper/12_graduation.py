# coding=utf-8

# 最新版的selenium(4.x.x)已经不支持PhantomJS。如要用PhantomJS，可用旧版本selenium。如pip install selenium==3.8.0。
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlwt
import time
import urllib.request
from urllib.request import urlopen, Request
import re
import os

# browser = webdriver.PhantomJS()
browser = webdriver.Chrome()
WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)

TRY = 5  # 下载试错
try_time = 0

MAX_PAGE = 2  # 爬取的页数
page = 0


def log(info, level=0):
    if level == 0:
        print("\033[31m" + info + "\033[0m")
    elif level == 1:
        print("\033[34m" + info + "\033[0m")


def download_file(download_url, filename):
    try:
        global try_time
        try_time = try_time + 1
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        response = Request(download_url, headers=headers)
        response = urlopen(response)  # 添加headers，解决某些网站的反爬虫
        file = open(filename + ".jpg", 'wb')
        file.write(response.read())
        file.close()

        if os.path.getsize(filename + '.jpg') == 0:
            print('*' * 5 + filename + 'download error' + '*' * 5)
    except urllib.error.HTTPError:
        # print('HTTP Error 403: Forbidden')
        log("TTP Error 403: Forbidden")
    # except Exception:
    #     print(Exception)
    #     if try_time < TRY:
    #         download_file(download_url, filename)
    #     else:
    #         print('**no paper**  '*5)


def normalize_name(name):
    name = name.replace(':', '')
    name = name.replace('/', '-')
    return name


# download_file('https://arxiv.org/pdf/1605.08695.pdf','paper ')

def get_paper_info(text):
    title, year, journal = "", "", ""
    if re.search(r'title={.*}', text):
        title = re.search(r'title={.*}', text).group()[7:-1]
    if re.search(r'year={.*}', text):
        year = re.search(r'year={.*}', text).group()[8:-1]
    if re.search(r'journal={.*}', text):
        journal = re.search(r'journal={.*}', text).group()[9:-1]
    print(title, year, journal)
    return title, year, journal


def search(topic, page):
    try:
        topic = 'grad_photo'
        # page = 1
        # 创建文件夹
        if not os.path.exists(topic):
            os.mkdir(topic)

        print('开始访问....')
        browser.get('https://flowus.cn/share/119430bd-b0b8-4321-962c-56fc6cb865a3')
        print('进入网站')
        WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.border-grey7')))
        list = browser.find_elements_by_css_selector(".border-grey7[data-test-id='drive-file-item']")

        # 没有结果
        if not list:
            print("查无结果")
            return

        for item in list:
            # TODO:引用命名
            # 点击
            # cite = item.find_element_by_css_selector("button[aria-label='Cite this paper']")
            browser.execute_script("arguments[0].click();", item)
            # cite.click()     # 直接点击可能出现：element click intercepted

            # 下载
            WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".justify-center a[rel='noreferrer']")))
            time.sleep(1)
            downdload = browser.find_element_by_css_selector(".justify-center a[rel='noreferrer']")
            browser.execute_script("arguments[0].click();", downdload)

            # 重新进入网站，是否之前的item还有效？无效：stale element reference: element is not attached to the page document。
            # browser.get('https://flowus.cn/share/119430bd-b0b8-4321-962c-56fc6cb865a3')
            # print('进入网站')

            # 回退
            WAIT.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "svg[class='icon flex-shrink-0 w-5 h-5 text-white sm:ml-0 ml-2 cursor-pointer']")))
            WAIT.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "*[class='icon flex-shrink-0 w-5 h-5 text-white sm:ml-0 ml-2 cursor-pointer']")))
            back = browser.find_element_by_css_selector(
                "svg[class='icon flex-shrink-0 w-5 h-5 text-white sm:ml-0 ml-2 cursor-pointer']")
            back.click()

            # browser.execute_script("arguments[0].click();", back)  # selenium不能够识别拼接的多个属性?在这里反而需要直接使用click()
            time.sleep(1)
            print('finish+1')

    except TimeoutException:
        log(str(TimeoutException))
        return search(None, None)
    # finally:  # 关闭之后，会出现Message: invalid session id
    #     browser.close()  # 只会关闭当前窗口


search(None, None)
browser.close()
