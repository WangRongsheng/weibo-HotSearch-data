import urllib.request #导入urllib.request库
import urllib.parse
from lxml import etree
import time

def weibo() :
    url = 'https://s.weibo.com/top/summary?'
    a = urllib.request.urlopen(url)  # 打开指定网址
    html = a.read()                # 读取网页源码
    html = html.decode("utf-8")   # 解码为unicode码
    # print(html)                # 打印网页源码

    tree = etree.HTML(html)
    list = tree.xpath(u'//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[@class="td-02"]')

    prefix = 'https://s.weibo.com'  # 微博域名
    weiboSummary = open((time.strftime("%Y-%m-%d-%H", time.localtime())) +".md", 'w')  # 打开并写入文件
    for index,item in enumerate(list):
        if index > 0:
            a_element = item.xpath('.//a')[0]
            title = a_element.text # 关键词
            href = urllib.parse.unquote(a_element.attrib.get('href')) # 链接
            href = href.replace("#", "%23") # 此处是对链接中的#号做一个编码转换，否则无法跳转指定关键词链接
            hot = item.xpath('./span')[0].text # 热度指数
            line = str(index) + "\t" + title + "\t" + hot + "\t" + prefix + href + "\n"
            print(line.replace("\n", ""))
            if href.find("javascript:void(0)") != -1:
                line = str(index) + "\t" + title + "\t" + hot
            #写入文件
            weiboSummary.write(line)
        else:
            title = '排名\t关键词\t热度\t链接\n'
            print(title.replace("\n",""))
            weiboSummary.write(title)
    weiboSummary.close()
    
#调用方法
weibo()
