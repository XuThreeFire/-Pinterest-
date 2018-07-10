#!usr/bin/env Python
# coding: utf-8
# from Climb_Pinterest_test import *

# 下载图片_一个文件
import os
import random
import asyncio
import requests
from concurrent.futures import *
from multiprocessing.pool import Pool
# 导入
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 添加下面这行代码:
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def thumb_to_img(word_path):
    print("当前word_path：\n", word_path)
    headers = {'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    async def down_a_thumb(url):
        print("下载链接：\n", url)
        # input("是否下载？\>>>")  # 下载过程的调试
        img_name = random.randint(1,100000)  # 产生随机图片名字
        img_content = requests.get(url, headers=headers,verify=False).content
        if not img_content:
            print("无效链接：")
        print("正在下载 {} 图片".format(img_name))
        with open(word_path +'/Img/{}.jpg'.format(img_name), 'wb') as img:
            img.write(img_content)

    url_list = []
    with open(word_path + '/Thumb_url' + '/all_thumb_url.text', 'r', encoding='utf-8') as f_list:
        for thumb in f_list.readlines():
            url_list.append(thumb.split('\n')[0])

    loop = asyncio.get_event_loop()
    task_list = [down_a_thumb(url) for url in url_list]
    loop.run_until_complete(asyncio.gather(* task_list))

if __name__ == "__main__":
    '''多协程'''
    headers = {'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    # word_path = "F:\Project\Python_Practice\Climb_Spider\bay_window"
    # word_path = word_path.replace('\\','/')

    cur_dir = os.getcwd()
    list_dir = os.listdir(cur_dir)
    dir_list = [cur_dir + '/' + i for i in list_dir if '.' not in i]

    # print(os.listdir(os.getcwd()))
    print(dir_list)
    # word_path = dir_list[0]  # 第1个
    # print("当前word_path：\n", word_path)
    # print("dir_list的个数：",len(dir_list))
    # thumb_to_img()
    # thumb_to_img(word_path)  # 一个任务
    '''多进程Process'''
    # with ProcessPoolExecutor(max_workers=None) as executor: #多进程
    #     executor(thumb_to_img, dir_list)
    with  Pool(4) as pool:
        pool.map(thumb_to_img, dir_list)

    print("下载完毕")
