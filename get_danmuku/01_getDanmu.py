#!/usr/bin/env python# -*- coding: utf-8 -*-#author tom

import os
import random
import re
import time

import requests
from lxml import etree

api_url = "https://dps.kdlapi.com/api/getdps/?secret_id=o0m6oalsegywinra696n&signature=9zx0e7gtow5ecvozw5ntz4wv94dwoo14&num=1&sep=1"

# 用户名密码认证(私密代理/独享代理)
username = "d2815234038"
password = "ogv8q3ye"

def get_new_proxy():
    proxy_ip = requests.get(api_url).text
    if not proxy_ip:
        raise Exception("获取代理失败，请检查API或网络连接")
    print(f"获取到新的代理IP: {proxy_ip}")
    return {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
    }

proxies = get_new_proxy()


headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}

# # 代理池（示例，实际使用时需替换为有效代理）
# proxy_pool = [
#     'http://202.101.213.210	:18796',
#     'http://124.124.124.124:3128',
#     'http://125.125.125.125:80'
# ]

# # 验证代理可用性（可选）
# def check_proxy(proxy):
#     try:
#         response = requests.get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
#         return response.status_code == 200
#     except:
#         return False


# # 过滤无效代理
# valid_proxies = [proxy for proxy in proxy_pool if check_proxy(proxy)]
# proxies = None
# print(len(valid_proxies))
# exit()
# for proxy in valid_proxies:
#     proxies = {
#         "http": proxy,
#         "https": proxy
#     }
#     break


#抓取函数
def get_danmu_from_url(url, max_retries=3):
    global proxies
    for _ in range(max_retries):
        try:
            res = requests.get(url, headers=headers, proxies=proxies)
            if res.status_code == 200:
                tree = etree.HTML(res.content)
                return tree.xpath('//d/text()')
        except Exception as e:
            print(f"请求失败: {e}, 正在尝试更换代理...")
        # 获取新代理并重试
        proxies = get_new_proxy()
        time.sleep(1)
    raise Exception(f"获取弹幕失败，已重试{max_retries}次")

def get_danmu_with_time_from_url(url, max_retries=3):
    global proxies
    for _ in range(max_retries):
        try:
            res = requests.get(url, headers=headers, proxies=proxies)
            if res.status_code == 200:
                tree = etree.HTML(res.content)
                danmus = []
                for d in tree.xpath('//d'):
                    text = d.text
                    timestamp = d.get('p').split(',')[0]  # 提取时间戳
                    danmus.append((text, timestamp))
                return danmus
        except Exception as e:
            print(f"请求失败: {e}, 正在尝试更换代理...")
        # 获取新代理并重试
        proxies = get_new_proxy()
        time.sleep(1)
    raise Exception(f"获取弹幕失败，已重试{max_retries}次")

def get_danmu_with_time_from_cid(cid, max_retries=3):
    url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={cid}'
    return get_danmu_with_time_from_url(url, max_retries)

def save_to_excel(data, filename):
    import pandas as pd
    df = pd.DataFrame(data, columns=['弹幕', '时间戳(秒)'])
    df.to_excel(filename, index=False)

# 获取aid以及cid
def get_video_id(bv, max_retries=3):
    global proxies
    for _ in range(max_retries):
        try:
            url = f'https://www.bilibili.com/video/{bv}'
            print(f"正在获取视频ID: {url}")
            html = requests.get(url, headers=headers, proxies=proxies)
            if html.status_code == 200:
                html.encoding = 'utf-8'
                content = html.text
                aid_regx = '"aid":(.*?),"bvid":"{}"'.format(url.split('/')[-1])
                cid_regx = '{"cid":(.*?),"page":1'
                aid = re.findall(aid_regx, content)[0]
                cid = re.findall(cid_regx, content)[0]
                return aid, cid
        except Exception as e:
            print(f"获取视频ID失败: {e}, 正在尝试更换代理...")
        # 获取新代理并重试
        proxies = get_new_proxy()
        time.sleep(1)
    raise Exception(f"获取视频ID失败，已重试{max_retries}次")

#主函数,其实所有是视频找到其id就能抓到所有的弹幕
def get_danmu_from_cid(cid):
    url='https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(cid)
    print(url)
    return get_danmu_from_url(url)

def get_danmu_from_bv(video_bv='BV1p7411Y7BC'):
    aid, cid = get_video_id(video_bv)
    return get_danmu_from_cid(cid)

def get_title_from_bv(video_bv='BV1p7411Y7BC'):
    global proxies
    url=f'https://www.bilibili.com/video/{video_bv}'
    res=requests.get(url,headers=headers, proxies=proxies).text
    pattern = r'class="video-title special-text-indent" .*?>(.*?)</h1>'
    title = re.findall(pattern,res)
    return title, url


def parse_contents(contents):
    pattern = r'/(BV.*?)/'
    bvs = re.findall(pattern,contents)
    bvs = set(bvs)
    # print(len(bvs),bvs)
    return bvs

def parse_contents(contents):
    pattern = r'/(BV.*?)/'
    bvs = re.findall(pattern,contents)
    bvs = set(bvs)
    # print(len(bvs),bvs)
    return bvs


def get_url_from_txt(filename):
    os.makedirs('danmu',exist_ok=True)
    with open(filename,'r', encoding='utf8') as file:
        contents = file.read()
        bvs = parse_contents(contents)
        # print(len(bvs),bvs)
        for i, bv in enumerate(bvs):
            if os.path.exists(f'danmu/{bv}.txt'):
                continue
            danmu_list = get_danmu_from_bv(bv)
            title, url = get_title_from_bv(bv)
            print(f"process {i+1}/{len(bvs)} video:", bv, title, url)

            with open(f'danmu/{bv}.txt','a+',encoding='utf8') as file:
                for danmu in danmu_list:
                    file.write(danmu+'\n')
            sleep_time = random.uniform(0.5, 10)
            print(f'解析后随机暂停{sleep_time:.2f}秒, 避免防爬机制')
            time.sleep(sleep_time)

def get_url_from_txt_to_excel(filename):
    os.makedirs('danmu',exist_ok=True)
    with open(filename,'r', encoding='utf8') as file:
        contents = file.read()
        bvs = parse_contents(contents)
        for i, bv in enumerate(bvs):
            if os.path.exists(f'danmu/{bv}.xlsx'):
                continue
            aid, cid = get_video_id(bv)
            title, url = get_title_from_bv(bv)
            print(f"process {i+1}/{len(bvs)} video:", bv, title, url)
            danmu_with_time = get_danmu_with_time_from_cid(cid)

            save_to_excel(danmu_with_time, f'danmu/{bv}.xlsx')
            sleep_time = random.uniform(0.5, 10)
            print(f'解析后随机暂停{sleep_time:.2f}秒, 避免防爬机制')
            time.sleep(sleep_time)
def main():
    # 保留原有功能
    # get_url_from_txt("danmuku_url-03.md")
    get_url_from_txt_to_excel("danmuku_url-03.md")


if __name__ == '__main__':
     main()

