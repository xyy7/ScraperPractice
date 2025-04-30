import requests


# ip = '120.24.76.81'
# proxies = {
#     'http':'http://'+ip,
#     'https':'http://'+ip  # 后面不能是https
# }


def request_douban(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.146 Safari/537.36',
    }

    try:
        response = requests.get(url=url,headers=headers, proxies={'https':'http://127.0.0.1:7890'})  # 增加了一个headers
        print('response',response)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        print(requests.RequestException)
        return None

# 设置系统代理之后，需要重启【似乎有没有开启系统代理并不重要】
url = 'https://www.google.com.hk'
# url = 'https://www.baidu.com'  # clash设置了系统代理，但是request没有proxies，此时不能访问==>重新启动之后，则可以访问
html = request_douban(url)
print(html)
