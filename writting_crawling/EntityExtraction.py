import pandas as pd
from collections import Counter
import jieba
import time
import re
import numpy as np
from tqdm import *

stopwords_path = './stopwords.txt'
stopwords_path_customize = './stopwords_added.txt'
stopwords = []
with open(stopwords_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        stopwords.append(line.strip())
with open(stopwords_path_customize,'r',encoding='utf-8-sig') as f:
    for line in f.readlines():
        stopwords.append(line.strip())

def get_continuous_content(x):
    return ''.join(eval(x))

def title_handle(showname):
    showname = re.sub('[a-zA-Z0-9《》]','',str(showname))
    s = jieba.cut(showname)
    s = ' '.join([i for i in s if i.strip() not in stopwords and len(i.strip())>0])
    return s

def get_cutted_text():
    file = pd.read_csv('./all_compo_fixed.csv')
    file['main'] = file['content'].apply(lambda x:''.join(eval(x)))
    file['title_words'] = file['title'].apply(lambda x:title_handle(x))
    file['main_words'] = file['main'].apply(lambda x:title_handle(x))
    writer = pd.ExcelWriter('./New.xlsx')
    file.to_excel(writer, 'sheet1')
    writer.save()

    # there might be memory error
    # file[:10000].to_excel('./New1.xlsx')
    # file[10000:].to_excel('./New2.xlsx')

def text_num_calculation(target_word, input_df):
    if len(re.findall(r'[\u4e00-\u9fff]+',target_word)) == 0:
        return 0
    else:
        df = input_df.loc[input_df['title_words'].str.contains(target_word),'main_words']
        return len(df)

def multiple(a,b):
    return a*b

def word_tf_idf(title_word, input_df, target_df):
    target_df.loc[target_df.isnull()] = '无'
    target_list = ' '.join(target_df).split(' ')
    dict_tmp = dict(Counter(target_list))
    total_num = len(target_list)
    result = pd.DataFrame()
    result['words'] = dict_tmp.keys()
    result['count'] = dict_tmp.values()
    result = result.loc[result['count']>1]
    if len(result)==0:
        del result
        return ' '
    else:
        result['freq'] = result['count'].apply(lambda x:x/total_num)
        result['N'] = result['words'].apply(lambda x:text_num_calculation(x,input_df))
        result['IDF'] = result['N'].apply(lambda x:np.log((len(input_df)+1)/(x+1))+1)
        result['TF-IDF'] = result.apply(lambda x:multiple(x.freq,x.IDF),axis=1)

        res = result.sort_values(by='TF-IDF', ascending=False).reset_index()
        del result
        return ' '.join(res['words'][:3])

def entity_list_get(word, input_df):
    df = input_df.loc[input_df['title_words'].str.contains(word), 'main_words']
    tmp = word_tf_idf(word, input_df, df)
    return tmp

def get_related_word(title_word_list, input_df):
    res = pd.DataFrame()
    res['word'] = title_word_list
    start = time.time()
    for i in tqdm(range(len(title_word_list))):
        word = title_word_list[i]
        df = input_df.loc[input_df['title_words'].str.contains(word), 'main_words']
        tmp = word_tf_idf(word, input_df, df)
        res.loc[res['word']==word, 'entities'] = tmp
    end = time.time()
    print('Running time: ', end-start)
    writer = pd.ExcelWriter('./Entity_result_top3_0.xlsx')
    res.to_excel(writer, 'sheet1')
    writer.save()

def indicator(word, freq):
    if (len(str(word))==1 and freq<5) or freq==1:
        return 0
    else:
        return 1

def get_word_freq(df):
    total = ' '.join(df['entities']).split(' ')
    res = pd.DataFrame()
    res['word'] = Counter(total).keys()
    res['values'] = Counter(total).values()
    res['freq'] = res['values'].apply(lambda x:x/len(total))
    writer = pd.ExcelWriter('./entity_freq2.xlsx')
    res.to_excel(writer, 'sheet1')
    writer.save()

if __name__ =='__main__':
    input_df = pd.read_excel('./New1.xlsx')
    input_df.loc[input_df['title_words'].isnull(), 'title_words'] = '无主题'
    title_wordlist = pd.DataFrame()
    title_word_list = ' '.join(input_df['title_words']).split(' ')
    title_wordlist['freq'] = Counter(title_word_list).values()
    title_wordlist['word'] = Counter(title_word_list).keys()
    title_wordlist['ind'] = title_wordlist.apply(lambda x:indicator(x.word, x.freq), axis=1)
    title_wordlist.sort_values(by='freq', ascending=False).reset_index()
    res = title_wordlist.loc[title_wordlist['ind']==1, 'word']
    get_related_word(list(res), input_df)