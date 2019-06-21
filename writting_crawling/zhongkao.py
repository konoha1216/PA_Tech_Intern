# -*- coding: utf-8 -*-

import pandas as pd
from pyquery import PyQuery as pq
import requests
import urllib.request as urllib2

def crawl_webPage(n):
    web_url='http://www.zhongkao.com/zxszw/ylw/index'
    # doc=pq(web_url)
    page_url=[]
    title_list=[]
    # content_list=[]
    for i in range(2,n+1):
        r = requests.get(web_url+'_'+str(i)+'.shtml')
        r.encoding = 'gb2312'
        doc = pq(r.content)
        for i in doc('.bk-listcon.right dl dd .ft16.bm5 a').items():
            if i.attr('title') is not None:
                page_url.append(i.attr('href'))
                title_list.append(i.attr('title'))

    # data = {'url': page_url, 'title': title_list}
    # df_all = pd.DataFrame(data)
    # df_all.to_csv('./zuowenwang.csv', index=False, encoding='utf_8_sig')
    # print(len(page_url), len(title_list))

    return page_url, title_list

def crawl_content(page, title):
    page_url, title_list = page, title
    flag = 0
    content_list = []
    for tmp in page_url:
        r = requests.get(tmp)
        r.encoding = 'gb2312'
        doc=pq(r.content)
        content_tmp=''
        for i in doc('.content.ft14 p').items():
            content_tmp+='\n' + i.text()
        content_list.append(content_tmp)
        flag+=1
        if flag%50 == 0:
            print(flag)
    # for i in range(len(title_list)):
    #     df_all.loc[len(df_all)]=[title_list[i],content_list[i]]
    print('title:', len(title_list))
    print('content:', len(content_list))

    data = {'title':title_list, 'content':content_list}
    df_all = pd.DataFrame(data)
    df_all.to_csv('./zhongkao2.csv',index=False,encoding='gb18030')

def main():
    page, title = crawl_webPage(59)
    print(len(page))
    crawl_content(page, title)

main()
