import json
import os
import random
import time
import pandas as pd
import requests
from requests.exceptions import RequestException


headers = {
    "Cookie": "datr=He2uZ5zrXowrTCGmeXoPp_jL; ig_did=BC50B356-4015-42F3-B59C-337200BC4D1E; ig_nrcb=1; ds_user_id=72170559054; ps_l=1; ps_n=1; mid=Z671dwALAAEa1I-G6yUczIrk2K7X; csrftoken=ZwB1YNTMAhpfyjx6Jzo0xkZG5O2STsVR; dpr=1.125; sessionid=72170559054%3Az1xiY2b29OuFEF%3A8%3AAYeZtICn03RzE2qKD0Kyn-2_hGCXNZLnMwmJ4u4n5Js; wd=407x780; rur=\"EAG\\05472170559054\\0541772512459:01f73e0b125dd5a7f2ab6dd1f77801ffd4c6ecb9b43d640609e8595c7b58db567e1173ec\"",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "X-Asbd-Id": "359341",
    "X-Bloks-Version-Id": "8cfdad7160042d1ecf8a994bb406cbfffb9a769a304d39560d6486a34ea8a53e",
    "X-Csrftoken": "ZwB1YNTMAhpfyjx6Jzo0xkZG5O2STsVR",
    "X-Fb-Friendly-Name": "PolarisProfileSuggestedUsersWithPreloadableQuery",
    "X-Fb-Lsd": "tPAH_2BGE8-_q3S6-cN8d2",
    "X-Ig-App-Id": "936619743392459"
}


proxy_dict = {
    'http': f'http://127.0.0.1:7890',
    'https': f'http://127.0.0.1:7890'
}

def log_error(error_message):
    """记录错误信息到日志文件"""
    with open("error_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")

def get_usr_data_from_url(url):
    try:
        response = requests.get(url, headers=headers, proxies=proxy_dict)
        response.raise_for_status()  # 检查请求是否成功
        html = response.json()

        # 验证返回的数据结构
        if 'data' not in html or 'user' not in html['data']:
            raise ValueError("返回的数据格式不正确，缺少关键字段")

        user_data = html['data']['user']
        num_of_tiezi = user_data['edge_owner_to_timeline_media']['count']
        num_of_fans = user_data['edge_followed_by']['count']
        num_of_watch = user_data['edge_follow']['count']
        return num_of_tiezi, num_of_fans, num_of_watch

    except RequestException as req_err:
        error_message = f"请求失败: {req_err} - URL: {url}"
        log_error(error_message)
        print(f"请求失败: {req_err}, 重试中...")
        time.sleep(5)  # 等待5秒后重试
        return get_usr_data_from_url(url)  # 递归重试

    except ValueError as val_err:
        error_message = f"数据格式错误: {val_err} - URL: {url}"
        log_error(error_message)
        print(f"数据格式错误: {val_err}")
        return None, None, None

    except Exception as e:
        error_message = f"未知错误: {str(e)} - URL: {url}"
        log_error(error_message)
        print(f"未知错误: {str(e)}")
        return None, None, None

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
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={usrname}"
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
        num_of_tiezi, num_of_fans, num_of_watch = get_data_from_username(username)  # 爬虫
        if num_of_tiezi is None:
            print(f"跳过 {username}，获取数据失败")
            continue
        sleep_time = random.uniform(1, 5)
        print(f'正在解析第{i}个博主：{username}, 解析后随机暂停{sleep_time:.2f}秒, 避免防爬机制')
        time.sleep(sleep_time)
        sheet["贴子数"][i] = num_of_tiezi
        sheet["粉丝数"][i] = num_of_fans
        sheet["关注数"][i] = num_of_watch

def main():
    """主函数"""
    sheet = get_sheet('ins.xls')
    process_sheet(sheet)
    save_sheet(sheet, 'ins_full.xls')

if __name__ == '__main__':
    main()
