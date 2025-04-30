# coding=utf-8

# 最新版的selenium(4.x.x)已经不支持PhantomJS。如要用PhantomJS，可用旧版本selenium。如pip install selenium==3.8.0。
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import xlwt
import time

# browser = webdriver.PhantomJS()
browser = webdriver.Chrome()
WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)

book = xlwt.Workbook(encoding='utf-8', style_compression=0)

sheet = book.add_sheet('蔡徐坤篮球', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '地址')
sheet.write(0, 2, '描述')
sheet.write(0, 3, '观看次数')
sheet.write(0, 4, '弹幕数')
sheet.write(0, 5, '发布时间')

n = 1


def search():
    try:
        print('开始访问b站....')
        # browser.get("https://www.bilibili.com/video/BV15b41157i4")
        browser.get("https://www.bilibili.com/")


        print('进入网站')

        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".nav-search-input")))
        submit = WAIT.until(EC.element_to_be_clickable(((By.CSS_SELECTOR, ".nav-search-btn"))))
        input.send_keys('蔡徐坤 篮球')
        submit.click()

        # 跳转到新的窗口
        print('跳转到新窗口')
        all_h = browser.window_handles
        browser.switch_to.window(all_h[1])
        # time.sleep(2)
        # browser.switch_to.window(all_h[0])
        # time.sleep(2)
        get_source()


    except TimeoutException:
        print(TimeoutException)
        return search()


def save_to_excel(soup):
    # find适用于xml？lxml(libxml) xpath(xmlpath) # 返回元素
    list = soup.select('.video-list .video-list-item a')  # 直接爬取，发现没有结果，说明应该是懒加载
    for item in list:
        print(item.get('href'))
        print()

    # # item_dec = item.find(class_='des hide').text
    # # item_view = item.find(class_='so-icon watch-num').text
    # # item_biubiu = item.find(class_='so-icon hide').text
    # # item_date = item.find(class_='so-icon time').text
    #
    # print('爬取：' + item_title)
    #
    # global n
    #
    # sheet.write(n, 0, item_title)
    # sheet.write(n, 1, item_link)
    # sheet.write(n, 2, item_dec)
    # sheet.write(n, 3, item_view)
    # sheet.write(n, 4, item_biubiu)
    sheet.write(n, 5, item_date)

    n = n + 1


def get_source():
    WAIT.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.video-list .video-list-item a')))  # 需要在获取到page_source前，就要等待好,但是等待不到？有可能是类名的问题？
    # time.sleep(10) # 显示等待和隐式等待的区别
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    print(html)
    print('到这')

    save_to_excel(soup)  # 解析和储存【每个网页是不一样的】


def main():
    try:
        search()
        time.sleep(1000)
    finally:
        browser.close()  # 只会关闭当前窗口
        # pass


if __name__ == '__main__':
    main()
    book.save('蔡徐坤篮球.xlsx')
