#!/usr/bin/env python# -*- coding: utf-8 -*-#author tom

import os
import random
import re
import time

import requests
from lxml import etree

api_url = "https://dps.kdlapi.com/api/getdps/?secret_id=olo6t8ninodibz6lwf3v&signature=trcfbvj79z1bjqh872yszw353q7ii1av&num=1&pt=1&sep=1"
proxy_ip = requests.get(api_url).text

# 用户名密码认证(私密代理/独享代理)
username = "d2466866551"
password = "ogv8q3ye"
proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
}


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
def get_danmu_from_url(url):
    res=requests.get(url,headers=headers, proxies=proxies)
    tree=etree.HTML(res.content)        
    return tree.xpath('//d/text()')

# 获取aid以及cid
def get_video_id(bv):
    url = f'https://www.bilibili.com/video/{bv}'
    html = requests.get(url, headers=headers, proxies=proxies)
    html.encoding = 'utf-8'
    content = html.text
    aid_regx = '"aid":(.*?),"bvid":"{}"'.format(url.split('/')[-1])
    cid_regx = '{"cid":(.*?),"page":1'
    aid = re.findall(aid_regx, content)[0]
    cid = re.findall(cid_regx, content)[0]
    return aid, cid

#主函数,其实所有是视频找到其id就能抓到所有的弹幕
def get_danmu_from_cid(cid):
    url='https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(cid)
    print(url)
    return get_danmu_from_url(url)

def get_danmu_from_bv(video_bv='BV1p7411Y7BC'):
    aid, cid = get_video_id(video_bv)
    return get_danmu_from_cid(cid)

def get_title_from_bv(video_bv='BV1p7411Y7BC'):
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

def main():
    get_url_from_txt("danmuku_url-03.md")

if __name__ == '__main__':
     main()
