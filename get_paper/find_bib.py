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
SEARCH_WEBSITE = None  # 支持谷歌和semantic scholars
MAX_PAGE = 2  # 爬取的页数
page = 0


def log(info, level=0):
    if level == 0:
        print("\033[31m" + info + "\033[0m")
    elif level == 1:
        print("\033[34m" + info + "\033[0m")


def download_file(download_url, filename):
    # 没有下载过，才需要进行下载
    if os.path.exists(filename + '.pdf'):
        return None

    try:
        global try_time
        try_time = try_time + 1
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        response = Request(download_url, headers=headers)
        response = urlopen(response)  # 添加headers，解决某些网站的反爬虫
        file = open(filename + ".pdf", 'wb')
        file.write(response.read())
        file.close()

        if os.path.getsize(filename + '.pdf') == 0:
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


# 如果是引用格式，转化成名字
def find_name(query):
    """
    eg:
    Lin K, Jia C, Zhang X, et al. DMVC: Decomposed Motion Modeling for Learned Video Compression[J]. IEEE Transactions on Circuits and Systems for Video Technology, 2022.
    DMVC: Decomposed Motion Modeling for Learned Video Compression
    :param query:cite format
    :return:paper name
    """
    pattern = 'et al\..*?\.'  # \.是转义字符；.*?是最短匹配
    res = re.search(pattern,query)
    if res is None:
        log('Could not find the paper name. Or the format is wrong.')
        return None
    span = res.span()
    name = query[span[0]+7:span[1]-4]
    return name


def search_semantic(query):
    try:
        print('开始访问....')
        browser.get("https://www.semanticscholar.org/search?q=" + query)
        print('进入网站')
        WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.result-page')))
        paper_list = browser.find_elements_by_css_selector(".result-page .cl-paper-row")
        print(len(paper_list))

        # 没有结果
        if not paper_list:
            print("查无结果")
            return

        for item in paper_list:
            # TODO:引用命名
            # 点击
            cite = item.find_element_by_css_selector("button[aria-label='Cite this paper']")
            browser.execute_script("arguments[0].click();", cite)
            # cite.click()     # 直接点击可能出现：element click intercepted

            # 复制
            WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".formatted-citation")))
            time.sleep(1)
            # new_html = browser.page_source
            # new_soup = BeautifulSoup(new_html, 'lxml')  # 不需要拿到在进行解析啦，直接可以拿出文字
            text = browser.find_element_by_css_selector(".formatted-citation").text  # 可能找不到文字
            print('text', text)

            title, year, journal = get_paper_info(text)
            name = year + '-' + journal + '-' + title
            name = normalize_name(name)
            print(name)

            # 关闭
            WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cl-button")))
            close = browser.find_element_by_css_selector('.cl-button')
            browser.execute_script("arguments[0].click();", close)

            # TODO:download pdf
            try:
                link = item.find_element_by_css_selector('.cl-paper-view-paper')  # 奇怪的一点：不是返回空，而是直接报错
            except selenium.common.exceptions.NoSuchElementException:
                log(name + 'Message: no such element: Unable to locate element: '
                           '{"method":"css selector","selector":".cl-paper-view-paper"}', 1)
                link = None

            if link:
                # for link in links:
                print(link.get_attribute('href'))
                url = link.get_attribute('href')
                if url.find('pdf') != -1:
                    # 可以下载pdf，但是有时候也会出现不成功
                    global try_time
                    try_time = 0

                    if not os.path.exists('papers'):
                        os.mkdir('papers')
                    download_file(url, 'papers' + '/' + name)
                    time.sleep(10)  # 不要太过频繁
                else:
                    log(name+':no paper found', 1)
            break  # 仅仅需要下载一次

    except TimeoutException:
        log(str(TimeoutException))
        return search_semantic(query)
    # finally:  # 关闭之后，会出现Message: invalid session id
    #     browser.close()  # 只会关闭当前窗口
d

# 搜索并下载
def search_and_download(query, download2file):
    pass


# 搜索并将引用保存到zotero
def search_and_not_download(query):
    passd


def cite_format_convert(raw_format, target_format):
    pass

search_semantic('DVC: An End-To-End Deep Video Compression Framework')
browser.close()
