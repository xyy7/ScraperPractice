import json
import os
import random
import time

import pandas as pd
import requests

headers = {
    "Cookie": "ig_did=C5DCC5E9-C53B-4AF2-AEF4-6CFE6B7589BD; csrftoken=aHN6FLVGc-00zkFXHQ_f8k; datr=ewO_ZxrKEQ4KyOwAUNCI7LkZ; ig_nrcb=1; mid=Z78DewALAAE3tLn32kGAbVQhO7Bb; wd=965x937",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
    "X-Asbd-Id": "359341", # 虽然每个人搜索的不一样，但还是可以使用的 
    "X-Csrftoken": "aHN6FLVGc-00zkFXHQ_f8k",
    "X-Ig-App-Id": "936619743392459",
    "X-Ig-Www-Claim": "0",
    "X-Requested-With": "XMLHttpRequest",
    "X-Web-Session-Id": "mo6x4u:ro53kg:d6m0zr"
}

proxy_dict = {
    'http': f'http://127.0.0.1:7890',
    'https': f'http://127.0.0.1:7890'
}

def get_usr_data_from_url(url):
    try:
        html = requests.get(url, headers=headers,proxies=proxy_dict).json()
        num_of_tiezi = html['data']['user']['edge_owner_to_timeline_media']['count']
        num_of_fans = html['data']['user']['edge_followed_by']['count']
        num_of_watch = html['data']['user']['edge_follow']['count']
        return num_of_tiezi, num_of_fans, num_of_watch
    except:
        import traceback
        traceback.print_exc()
        with open("ins.json", "w", encoding="utf-8") as f:
            json.dump(html, f, ensure_ascii=False, indent=2)
        os.system("pause")
        exit()

def get_sheet(filename):
    sheet = pd.read_excel(filename)
    return sheet


def save_sheet(sheet, filename):
    sheet.to_excel(filename)

def get_data_from_username(usrname):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={usrname}"
    # print(url)
    num_of_tiezi, num_of_fans, num_of_watch = get_usr_data_from_url(url)
    print(f"{usrname} 贴子数：{num_of_tiezi}, 粉丝数：{num_of_fans}, 关注数：{num_of_watch}")
    return num_of_tiezi, num_of_fans, num_of_watch

def process_sheet(sheet):
    sheet["贴子数"] = [0] *len(sheet["User ID"])
    sheet["粉丝数"] = [0] *len(sheet["User ID"])
    sheet["关注数"] = [0] *len(sheet["User ID"])
    for i, username in enumerate(sheet["Username"]):
        num_of_tiezi, num_of_fans, num_of_watch = get_data_from_username(username) # 爬虫
        sleep_time = random.uniform(1, 5)
        # print(i, username, "sleep:",sleep_time,' s')
        print(f'正在解析第{i}个博主：{username}, 解析后随机暂停{sleep_time:.2f}秒, 避免防爬机制')
        time.sleep(sleep_time)  
        sheet["贴子数"][i] = num_of_tiezi
        sheet["粉丝数"][i] = num_of_fans
        sheet["关注数"][i] = num_of_watch

def main():
    sheet = get_sheet('ins.xls')
    process_sheet(sheet)
    save_sheet(sheet, 'ins_full.xls')

if __name__ == '__main__':
     main()

