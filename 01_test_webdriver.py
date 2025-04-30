import os
import re
import time
import urllib.request
from urllib.request import Request, urlopen

import selenium
import xlwt
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://www.instagram.com/brinacocker")

WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)
