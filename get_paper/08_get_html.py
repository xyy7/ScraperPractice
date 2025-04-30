import requests
from bs4 import BeautifulSoup
import xlwt



def request_douban(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.146 Safari/537.36',
    }

    try:
        response = requests.get(url=url, headers=headers)  # 增加了一个headers
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

url = 'https://www.google.com.hk'
# url = 'https://www.baidu.com'
html = request_douban(url)
print(html)