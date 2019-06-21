# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import pandas as pd
from pyquery import PyQuery as pq
# df_all = pd.DataFrame(columns=['title', 'content'])

def crawl_webPage(n):
    web_url='https://www.99zuowen.com/yilunwen/chuzhong/'
    # doc=pq(web_url)
    page_url=[]
    title_list=[]
    # content_list=[]
    for i in range(1,n+1):
        doc = pq(web_url+'826-'+str(i)+'.html')
        for i in doc('.article li a').items():
            if i.attr('title') is not None:
                page_url.append(i.attr('href'))
                title_list.append(i.attr('title').strip('<b>'))
    return page_url, title_list

def crawl_content(page, title):
    page_url, title_list = page, title
    flag = 0
    content_list = []
    for tmp in page_url:
        doc=pq(tmp)
        content_tmp=''
        for i in doc('.content div p').items():
            content_tmp+=i.text()
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
    df_all.to_csv('./zuowen.csv',index=False,encoding='utf_8_sig')

def main():
    page, title = crawl_webPage(9)
    print(len(page))
    crawl_content(page, title)

main()
