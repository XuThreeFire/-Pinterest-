#!urs/bin/env Python
#coding: utf-8
import re
import os
import sys
import time
import random
import requests
import asyncio
from multiprocessing.pool import Pool
from toolz.curried import *
# 如何防止没玩没了的Warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 添加下面这行代码:
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
""" 一、实现：输入keyword,保存500个链接为一个文件,默认一个keyword,两次pin迭代
    一、具体实现
    1、keyword转化为主页 ok
    2、一个url变成pin存储在总pin内  Ok
    3、将总pin按照每100个保存起来 OK
    4、一个pin变成下载链接 OK
    5、一个pin文件对应同名的下载链接文件 OK
    6、收集所有的链接保存按照500个保存
"""

# 1、keyword转化为主页
"""入：key_word,出：url"""
def key_to_url(key_world):
    """
    输入搜索关键词：如"word1 worrd2 word3"
    返回搜索url
    """
    key_list = key_world.split(' ')  # 获取关键词列表
    # 第一段url
    base_url = "https://www.pinterest.jp/search/pins/?q="
    # 第二段url
    q = len(key_list)>1 and '%20'.join(key_list) or '%20'.join(key_list)
    rs = ['&rs=typed']
    # 第三段url
    for word in key_list:
        rs.append("&term_meta[]={}%7Ctyped".format(word))
    rs = ''.join(rs)
    # 合并后的url
    url = base_url + q + rs

    print(url)
    return url

# 根据关键词创建文件系统
# Pin_id,Thumb_url,Img
def key_to_dir_path(key_world, localpath):
    world = key_world.replace(' ', '_')  #
    path = localpath.replace('\\', '/') +'/'+ world
    # 创建文件系统
    if not os.path.exists(path):
        os.mkdir(path)
        os.mkdir(path + '/Pin_id')
        os.mkdir(path + '/Thumb_url')
        os.mkdir(path + '/Img')
        print("新建路径：", path)
    else:
        print("路径已存在：", path)
    # 改变工作路径到word文件夹
    os.chdir(path)


#将pin写入指定文件
def pin_to_Pin_id_all_pin_text(pin_list):
    file_path = 'Pin_id' + '/all_pin_id.text'  # OK
    with open(file_path, 'a', encoding='utf-8') as f1:
        for i in pin_list:
            f1.write(i + '\n')
    print("{} 个Pin_list存储成功！".format(len(pin_list)))
    print("存储路径：", file_path)
    return True


# 2、一个url变成pin存储在总pin内
# async def url_to_pin(url):
def url_to_pin(url):
    # 1、获取不重复的pin
    txt = requests.get(url, headers=headers, verify=False).text
    pin_list = re.findall(r'("id": "\d{18}")', txt)  #
    if pin_list:
        print("Find some Pin_id: 个".format(len(set(pin_list))))
        for i in set(pin_list):  # 去除'id'
            all_pin_list.append(i[-19:-1])
    else:
        print("Not find any Pin_id.")
        # return None  # 没有发现

    # 2、存储pin
    pass

# 3、将总pin按照每100个保存起来
def all_to_100(file_path):
    with open(file_path, 'r', encoding='utf-8') as f1:
        all_content = f1.readlines()

    print("文件：{} \n行数:{}".format(file_path, len(all_content)))

    n = len(all_content)//100 + 1

    for index in range(n):
        new_file = file_path.replace('.text', '{}.text'.format(index))
        with open(new_file, 'w', encoding='utf-8') as f1:
            for i in range(100):  # 每次写一百行
                place = index*100+i
                if place < len(all_content):
                    f1.write(all_content[place])
                else:
                    break
    print("拆分成功！！！")

# 4、一个pin变成下载链接
"""输入pin, 返回736x链接地址列表"""
async def a_pin_to_thumb(pin):
    if not isinstance(pin, str):
        pin = str(pin)
    url = base_pin_url + pin
    if '\n' in url:
        print("错误的链接：包含有换行")
    if ' ' in url:
        print("错误的链接：包含有空格")

    # url = url.strip(' ')
    # print("开头：{} 结尾{}".format(url[0:1], url[-2:-1]))
    #  获取内容
    pin_id_text = requests.get(url, headers=headers, verify=False).text
    # 获取thumb
    regex = r'(https://i\.pinimg\.com/736x/.{0,100}\.jpg)'
    pin_https = re.findall(regex, pin_id_text)
    aset = set(pin_https)
    if not pin_https:
        print("pin链接:",url)
        print("Can't find some https")
        return None
    else:
        print("Find {} 个 736x 链接地址！\n".format(len(aset)))
        for i in aset:
            thumbList.append(i)
    # return list(aset)


#将thumb写入指定文件
def write_all_thumb_text(thumb_list):
    file_path = 'Thumb_url' + '/all_thumb_url.text'  # OK
    with open(file_path, 'a', encoding='utf-8') as f1:
        for i in thumb_list:
            f1.write(i + '\n')
    print("{} 个Thunmb_url存储成功！".format(len(thumb_list)))
    print("存储路径：", file_path)

    return True
# 5、一个pin文件对应同名的下载链接文件
pass

# 6、收集所有的链接保存按照500个保存
def all_pin_to_all_thumb():
    p_file = 'Pin_id' + '/all_pin_id0.text'  # 从第一个
    # t_file = 'Thumb_url' + '/all_thumb_url.text'
    with open(p_file, 'r', encoding='utf-8') as f1:
        p_list = f1.readlines()
    p_list = [i.split('\n')[0] for i in p_list]

    print("当前路径：", os.getcwd())
    print("开始将all_pin_id.text转化为图片链接！")
    loop = asyncio.get_event_loop()
    task_list = [a_pin_to_thumb(pin) for pin in p_list]
    loop.run_until_complete(asyncio.gather(*task_list))
    print("当前路径：", os.getcwd())
    print("转化为图片链接成功！")




""" 二、实现：输入keyword,和个数N,下载N张图片,默认500
    二、具体实现
    1、根据keyword查找文件夹,返回图片链接的文件全路径
    2、保存图片到同样keyword的文件夹下
"""
def main(key_word):
    # 设置公共变量
    # localpath = "F:\Project\Python_Practice\Climb_Spider".replace('\\', '/')
    localpath = "F:\Piture\Pinter".replace('\\', '/')
    # key_word = 'bikini' # OK
    # key_word = 'girl'
    # key_word = 'beautiful girl'
    # key_word = 'dog'
    # key_word = 'bay window'
    # key_word = 'pretty girl'
    # key_word = 'love'
    # key_word = 'beautiful woman'
    # key_word = 'nordic liviroom'
    # base_pin_url = "https://www.pinterest.jp/pin/"

    # 1.1、keyword转化为主页``
    url = key_to_url(key_word)
    # 1.2、文件系统
    '''测试文件路径'''
    key_to_dir_path(key_word, localpath) # OK

    # 2、一个url变成pin存储在总pin内
    headers = {'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    # all_pin_list = []  # 存储pin 全局
    url_to_pin(url)  # 获取pin 存在 all_pin_list
    # 判断是不是在关键词路径下
    if 'Img' not in str(os.listdir(os.getcwd())):
        print("不在关键词路径下！")
        key_to_dir_path(key_word, localpath) # OK

    pin_to_Pin_id_all_pin_text(all_pin_list)  # 存储pin

    # 3、将总pin按照每100个保存起来 OK
    words = key_word.replace(' ', '_')
    f_path = localpath + '/' + words + '/Pin_id/all_pin_id.text'
    all_to_100(f_path)

    # 4、一个pin变成下载链接 OK
    """输入pin, 返回736x链接地址列表"""
    # a  = 456059899754479191
    # pin = str(a)
    # thumbList = []
    # a_pin_to_thumb(pin)  # 存储在thumbList

    # 6、收集所有的链接保存按照500个保存
    # thumbList = []
    all_pin_to_all_thumb()
    write_all_thumb_text(thumbList)  # 存入对应的文件
    # a_pin_to_thumb(pin)''

# 全局变量

thumbList = []
all_pin_list = []  # 存储pin
headers = {'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
base_pin_url = "https://www.pinterest.jp/pin/"

if __name__ == "__main__":
    # key_list = ['nordic bedroom', 'house', 'bookroom', 'study room',
    # 'sexy girl']
    # key_list = ['美女', 'football baby', '足球宝贝', 'sexy lady','football girl', 'beauty teacher', 'sexy beauty', 'youth girl']
    # key_list = ['']
    if not key_list:
        print("Can't find any key word.")
        sys.exit("Please check the word that you give.")
    with Pool(4) as pool:  # 开启四个线程爬取
        pool.map(main, key_list)
    print("End","**"*20,'ENd')
    # main()


# END APP
