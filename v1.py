# -*- coding=UTF-8 -*-
# 需要requests、bs4、pandas库
import os
import time
import requests
import bs4
import pandas as pd

def crawl():
    '''
    爬虫模块
    返回r，即网页源码
    '''
    
    url = "https://s.weibo.com/top/summary?cate=realtimehot"
    headers={
        'Host': 's.weibo.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://weibo.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout =10)
        return r
    except:
        return 0
    # 爬虫结束

def data_processing(r):
    '''
    数据处理模块
    返回data，即｛标题：热度｝字典
    '''

    html_xpath = bs4.BeautifulSoup(r.text,'html.parser')
    data = {}
    title = []
    hot = []
    https = html_xpath.find_all('td',attrs={'class':'td-02'})
    for i in range(len(https)):
        tag = https[i].text.split('\n')
        if i == 0:
            tag[2] = '0'
        title.append(tag[1])
        hot.append(tag[2])
        data['标题'] = title
        data['热度'] = hot
    data = pd.DataFrame(data)
    return data
    # 处理结束，标题和热度都存在字典data中

def build_path():
    '''
    路径生成模块
    返回path，即md文件最终路径
    '''
    
    # 解决存储路径
    time_name = time.strftime('%Y{y}%m{m}%d{d}%H{h}',time.localtime()).format(y='年', m='月', d='日',h='点')
    year_path = time.strftime('%Y{y}',time.localtime()).format(y='年')
    month_path = time.strftime('%m{m}',time.localtime()).format(m='月')
    day_month = time.strftime('%d{d}',time.localtime()).format(d='日')
    all_path = "./data/" + year_path + '/'+ month_path + '/' + day_month
    if not os.path.exists(all_path):
        # 创建多层路径
        os.makedirs(all_path)
    # 最终文件存储位置
    root = all_path  + "/"
    path = root + time_name + '.csv'
    return path

def write_file(data,path):
    '''
    写入文件模块
    '''
    data.to_csv(path,encoding='utf-8-sig') #编码格式必须为 utf-8-sig 不能为 utf-8

def main():
    '''
    主函数
    '''
    r = crawl()
    if r :
        write_file(data_processing(r),build_path())
        print('获取热搜完毕，三秒后关闭…')
    else :
        print('爬虫失败，检查网络')
    time.sleep(3)
    
if __name__ == '__main__':
    main()
