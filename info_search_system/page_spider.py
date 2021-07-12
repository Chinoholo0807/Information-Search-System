import json
import requests
from lxml import etree
from config import *
import re
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}
doc_cnt = 0
url_list = list()

if not os.path.exists(spider_doc_folder):  # 创建存储的文件夹
    os.mkdir(spider_doc_folder)

for i_page in range(1, 50):  # 爬取存储url的页面
    base_url = 'http://so.news.cn/getNews?keyword=%s&curPage=%d&sortField=0&searchFields=1&lang=en' % (
        topic, i_page)
    response = requests.get(base_url, headers)
    urls = re.findall('(http:.+?htm)', response.text)  # url提取
    for url in urls:  # 存储url
        url_list.append(url)

for url in url_list:
    response = requests.get(url, headers)
    tree = etree.HTML(response.text)
    try:
        p_list = tree.xpath('/html/body/div[5]/div[4]/p')
    except:
        continue
    path = spider_doc_folder + '/' + '%04i.json' % doc_cnt
    fp = open(path, 'w', encoding='utf-8')
    try:
        title = tree.xpath('/html/body/div[5]/h1/text()')[0]
        time = tree.xpath('/html/body/div[5]/div[1]/i[2]/text()')[0]
    except:
        continue
    content = ""
    for p in p_list:
        try:
            p_content = p.xpath('.//text()')[0]
            content = content + p_content + '\n'
        except:
            continue
    if content == '':
        continue

    doc_dict = dict()
    doc_dict['title'] = title.strip()
    doc_dict['time'] = time
    doc_dict['url'] = url
    doc_dict['content'] = content
    json.dump(doc_dict, fp=fp, ensure_ascii=False, indent=4)
    doc_cnt = doc_cnt + 1
    print(path + ' - ' + title + ' save..')
