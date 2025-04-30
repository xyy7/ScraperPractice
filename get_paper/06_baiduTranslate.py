from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


browser = webdriver.Chrome()
browser.get('https://fanyi.baidu.com/?aldtype=16047#auto/zh/')
wait = WebDriverWait(browser, 10,2)

# 可恶的按钮
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.desktop-guide-close')))  # 如果找不到，会有timeoutException
button.click()

kw = wait.until(EC.presence_of_element_located((By.ID, 'baidu_translate_input')))

list = ['中文', '英文', '德文']
for word in list:
    kw.send_keys(word)
    time.sleep(1)
    result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ordinary-output>span')))
    print(result.text)
    kw.clear()
    time.sleep(1)
print(kw, button)
