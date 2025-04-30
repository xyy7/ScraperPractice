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
import concurrent
import os
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup


def header(referer):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.146 Safari/537.36',
        'Referer': '{}'.format(referer),
    }

    return headers




def get_paper_name():

    return None

def


topic = None
url = 'https://www.semanticscholar.org/search?q='+topic+'&sort=relevance'

with open('paper.pdf', 'wb') as f:
    pdf = requests.get(item, headers=header(item)).content
    print(pdf)
    f.write(pdf)