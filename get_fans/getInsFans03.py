import random
import re
import time
import warnings

import pandas as pd
import requests
from requests.exceptions import RequestException

warnings.filterwarnings("ignore")


# # 提取代理API接口，获取1个代理IP
# api_url = "https://dps.kdlapi.com/api/getdps/?secret_id=olo6t8ninodibz6lwf3v&signature=trcfbvj79z1bjqh872yszw353q7ii1av&num=1&pt=1&sep=1"

# # 获取API接口返回的代理IP
# proxy_ip = requests.get(api_url).text

# # 用户名密码认证(私密代理/独享代理)
# username = "d2466866551"
# password = "ogv8q3ye"
# proxies = {
#     "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
#     "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
# }
# print(proxy_ip)

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Cookie": "_ga=GA1.1.581329718.1742440136; _cc_id=863d96150f3fccf1993d9ecd7e596841; panoramaId_expiry=1742526537615; panoramaId=7ce4161f481c2626dc01801f8a59a9fb927a4d6447f6ce70fe6cab6d5855917a; panoramaIdType=panoDevice; usprivacy=1N--; sharedid=e371dbe3-c215-4b5e-b0f0-1cd97603b09d; sharedid_cst=kSylLAssaw%3D%3D; __qca=P0-924408424-1742440144924; cto_bundle=0sLeLl9uZHBYWkZLanF6VzNVaWxyeVltVzBHOXRBMzhWZk53d09iNjVMTE9VVGdoS2F0ZTF0dVpRWE0xeDBPb2h4WnhhV25QMk9HYmtYY2syUDNENnEzR1JWZzFnVlpaTm9OWTJyWHNtMjFOSG9wMldyUVdxR0xvSUVxbHFDeTRuJTJCNnlvMXBWUkl1aUglMkZnRE8lMkYlMkYlMkZXJTJGSVNxRFElM0QlM0Q; cto_bidid=bT_kGV9MQyUyRkVhZk9BMzUyS01qNlZZUlQ0TkNzOHh2Rm9ySFVqb056SEx6VEZsalhidkFSMTNSa1JiQzIlMkI0c1MwWldDZzFncFo1YWhCYjIyeHIzU3E5SVVMeW9OWkp0ckUxSm5yRCUyRlNVc0NrNkc5MCUzRA; FCNEC=%5B%5B%22AKsRol8USmL8MYEZaII79eGt-VsE4_N7XMId-1aV5POpeB9pmupXMKqNWquWCfKN3I37M0XvHuAHCMf4OK2HGgjvKyybgNetnEl56hQ6CU546GBGH4blxTKc5L6r9R69a_YLZDJTJh21z5vA7kONQ2oGcxyUHu-CVA%3D%3D%22%5D%5D; cf_clearance=XpjCQ2UGnYHvaU0NXwBUBWI8sMKFDIAhhb_2a9IzWZY-1742457399-1.2.1.1-XX6C7cXfQHsLQtSoTIWNxMYfyrM.w4Po2KeVto5AKKEyBVkEIbv67Cb0PdgCZHmrdzJHJAWfa3motc3VaffhQvN47b5wmfvglDAF1DnpDQ2L9dVOlVv.FjPtzemquWUWQyt6B1tj92q4KIH6s_NpZusqkzBvg4foSBXaz.VjM0EDnWyrbJSYYcd8nLtSml.Env9qMddEhYBG64ZSMM4W7j2hr_b3jWIRllucINWdgGp3ghbGpyAgKELWsoE5hvtFq86kVpIbJvBnIr_tJ_CzzW6gkL4L9z4IACjxxpNg_DPY0Wz34rQIRff.95fgkGwhZqSTN1IZXcPlBy0kPt8TjM04IBbMV8Kpgv4WXJkPH7U; _ga_GC2VPDBYKB=GS1.1.1742453658.4.1.1742457399.0.0.0; __gads=ID=c5cba9bd7e4d4dbd:T=1742440137:RT=1742457399:S=ALNI_MbUY4wCJ1aiRCUCjc6z3hEjdh28og; __gpi=UID=0000106a4a9bb63d:T=1742440137:RT=1742457399:S=ALNI_MbhgT9BwrMtwO0wBvoxe9h4_zOfDA; __eoi=ID=d53f7074b561926c:T=1742440137:RT=1742457399:S=AA-Afjay-e2ZVlkAYZg3W6WFneI8",
    "Pragma": "no-cache",
    "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


proxy_dict = {
    'http': f'http://127.0.0.1:7890',
    'https': f'http://127.0.0.1:7890'
}

def check_proxy(proxy):
    url = "http://www.google.com"  # 可以换成其他测试网址
    proxies = proxy
    
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"代理 {proxy} 有效")
            return True
        else:
            print(f"代理 {proxy} 无效，状态码：{response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"代理 {proxy} 无效，错误信息：{e}")
        return False

# if check_proxy(proxy_dict):
#     print(proxy_dict,"代理是有效的")
# else:
#     print(proxy_dict,"代理是无效的")
# # exit()

def log_error(error_message):
    """记录错误信息到日志文件"""
    with open("error_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")
        print(error_message)

def get_usr_data_from_url(url):
    try:
        response = requests.get(url, headers=headers, proxies=proxy_dict)
        response.raise_for_status()  # 检查请求是否成功
        html_content = response.text

        results = re.findall(r'"userInteractionCount": (\d+) }',html_content)
        if results is None or len(results) != 3:
            error_message = f"{url} 找不到对应粉丝数据"
            log_error(error_message)
            return 0, 0, 0
        # return num_of_tiezi, num_of_fans, num_of_watch
        return int(results[2]), int(results[1]), int(results[0])

    except RequestException as req_err:
        error_message = f"请求失败: {req_err} - URL: {url}，该用户可能不存在于https://imginn.com/，或者网络有问题"
        log_error(error_message)
        return 0, 0, 0

def get_sheet(filename):
    """读取Excel文件"""
    try:
        sheet = pd.read_excel(filename)
        return sheet
    except Exception as e:
        log_error(f"读取文件失败: {str(e)} - 文件: {filename}")
        print(f"读取文件失败: {str(e)}")
        exit()

def save_sheet(sheet, filename):
    """保存数据到Excel文件"""
    try:
        sheet.to_excel(filename)
    except Exception as e:
        log_error(f"保存文件失败: {str(e)} - 文件: {filename}")
        print(f"保存文件失败: {str(e)}")
        exit()

def get_data_from_username(usrname):
    """获取用户的社交数据"""
    url = f"https://imginn.com/{usrname}/"
    num_of_tiezi, num_of_fans, num_of_watch = get_usr_data_from_url(url)
    if num_of_tiezi is None:
        return 0, 0, 0  # 返回默认值，以防数据获取失败
    print(f"{usrname} 贴子数：{num_of_tiezi}, 粉丝数：{num_of_fans}, 关注数：{num_of_watch}")
    return num_of_tiezi, num_of_fans, num_of_watch

def process_sheet(sheet):
    """处理整个Excel表格"""
    sheet["贴子数"] = [0] * len(sheet["User ID"])
    sheet["粉丝数"] = [0] * len(sheet["User ID"])
    sheet["关注数"] = [0] * len(sheet["User ID"])
    for i, username in enumerate(sheet["Username"]):
        print(f"https://imginn.com/{username}/")

def main():
    """主函数"""
    sheet = get_sheet(r'F:\szu18-onedrive\OneDrive - email.szu.edu.cn\CodeRep\Work-06_scrapper\get_fans\ins.xls')
    process_sheet(sheet)
    save_sheet(sheet, r'F:\szu18-onedrive\OneDrive - email.szu.edu.cn\CodeRep\Work-06_scrapper\get_fans\ins-full.xls')

if __name__ == '__main__':
    main()
