import pandas as pd
import numpy as np
import random

def stopwordslist(path):
    # path = 'stopword.txt'
    stopwords = [line.strip() for line in open(path, encoding='utf-8-sig').readlines()]
    return stopwords
stopwords = stopwordslist('stopword.txt')


def compo_dictionary(path):
    compo = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        for line in f.readlines():
            compo.append(line)
    compo_dict = []
    for cur in compo:
        compo_dict.append(eval(cur.strip('\n')))
    return compo_dict
compo_dict = compo_dictionary('jieba_data_fixed_startend.txt')

def read_entities(path):
    df = pd.read_excel(path)
    wordEntitiesDict = {}
    for i in range(df.shape[0]):
        if df.loc[i,'word'] in wordEntitiesDict:
            print('redundant:', df.loc[i,'word'])
        else:
            wordEntitiesDict[df.loc[i,'word']] = df.loc[i,'entities'].split(' ')
    return wordEntitiesDict
wordEntitiesDict = read_entities('EntityResult.xlsx')

def checkTitle(compo_dict,stopwords):
    # check if any title is null
    test_compo = []
    for cur in compo_dict:
        cur_title = []
        for item in cur['title']:
            if item not in stopwords:
                cur_title.append(item)
        test_compo.append({'pmid':cur['pmid'], 'title':cur['title']})

    for zuowen in test_compo:
        if len(zuowen['title'])==0:
            print('this compo has no meaningful title:', zuowen['title'])
    return test_compo
test_compo = checkTitle(compo_dict,stopwords)

def check_entities_num(test_compo, wordEntitiesDict):
    activate_num = []
    for zuowen in test_compo:
        cur_title = zuowen['title']
        cur_activate_num = 0
        cur_entities = []
        for item in cur_title:
            if item in wordEntitiesDict:
                cur_entities+=wordEntitiesDict[item]
                cur_activate_num+=1
        activate_num.append(cur_activate_num)
        zuowen['entities'] = cur_entities
        zuowen['activate_num'] = cur_activate_num

    #check if any title doesn't have related entities
    num = 0
    for n in activate_num:
        if n==0:
            num+=1
    print("we have ",num, " titles that don't have related entities")
    # give the first example of this case: pmid==3589, title=别说"不"
    for zuowen in test_compo:
        if zuowen['activate_num']==0:
            print('one example of them is: ',zuowen)
            break
    return test_compo
test_compo = check_entities_num(test_compo, wordEntitiesDict)

def count_entitiesNumber(test_compo):
    # count how many entities each title is connected with
    entities_count = []
    for zuowen in test_compo:
        if zuowen['title']==0:
            entities_count.append(0)
        else:
            cur_list = list(set(zuowen['entities']))
            entities_count.append(len(cur_list))
    # we have tested that the most connected entities number is 45!!!
    count0,count5,count10,count15,count20,count25,count30,count35,count40,count45 = 0,0,0,0,0,0,0,0,0,0
    for count in entities_count:
        if count==0:count0+=1
        if count>0 and count<=5:count5+=1
        if count > 5 and count <= 10: count10 += 1
        if count > 10 and count <= 15: count15 += 1
        if count > 15 and count <= 20: count20 += 1
        if count > 20 and count <= 25: count25 += 1
        if count > 25 and count <= 30: count30 += 1
        if count > 30 and count <= 35: count35 += 1
        if count > 35 and count <= 40: count40 += 1
        if count > 40 and count <= 45: count45 += 1
    print('0: ',count0)
    print('0-5: ', count5)
    print('5-10: ', count10)
    print('10-15: ', count15)
    print('15-20: ', count20)
    print('20-25: ', count25)
    print('25-30: ', count30)
    print('30-35: ', count35)
    print('35-40: ', count40)
    print('40-45: ', count45)
    return 0
count_entitiesNumber(test_compo)

# check if one compo has '' in its related entities
for zuowen in test_compo:
    if '' in zuowen['entities']:
        print(zuowen)

def frequency_sort(path, test_compo):
    df2 = pd.read_excel(path)
    score_dict = {}
    for i in range(df2.shape[0]):
        score_dict[df2.loc[i,'word']] = df2.loc[i,'score']

    # four composition whose pmid=5503,10033,10040,691, have null related entities contained under their 'entities' keys,
    #  so we need to remove these nulls
    for zuowen in test_compo:
        if zuowen['pmid']==5503: zuowen['entities'] = zuowen['entities'][2:]
        if zuowen['pmid']==10033: zuowen['entities'] = zuowen['entities'][:8]+zuowen['entities'][10:]
        if zuowen['pmid']==10040: zuowen['entities'] = zuowen['entities'][8:]
        if zuowen['pmid'] == 691: zuowen['entities'] = zuowen['entities'][2:]
    # rank the related entities for each composition, based on the netities's frequency score
    for zuowen in test_compo:
        entities = zuowen['entities']
        if len(entities)>10:
            cur_dict={}
            for item in entities:
                cur_dict[item] = score_dict[item]
            ascend_list = sorted(cur_dict,key=cur_dict.__getitem__) # fron ones are with small scores
            descend_list = sorted(cur_dict,key=cur_dict.__getitem__,reverse=True) # fron ones are with big scores
            zuowen['Last10'] = ascend_list[:10]
            zuowen['Top10'] = descend_list[:10]
        else:
            zuowen['Last10'] = entities
            zuowen['Top10'] = entities
    return test_compo
test_compo = frequency_sort('entity_freq.xlsx',test_compo)

def calculate_intersection(test_compo, mysize):
    myrand = np.random.randint(len(test_compo)-1, size=mysize)
    my_jaccard = []
    for i in myrand:
        for j in myrand:
            if i!=j:
                set1 = set(test_compo[i]['Top10'])
                set2 = set(test_compo[j]['Top10'])
                l1 = len(set1.intersection(set2))
                l2 = len(set1.union(set2))
                if l2==0:
                    continue
                cur_jaccard = l1/l2
                my_jaccard.append(cur_jaccard)
    return len(my_jaccard), np.mean(my_jaccard)
thislength, thismean = calculate_intersection(test_compo, 1000)
print(len(thislength), np.mean(thismean))

def lastprocess(compo_dict, test_compo, which, valid_ratio=0.1, iftest = False, test_ratio=0.1):
    # which = 'Top10' or 'Last10'
    for i in range(len(compo_dict)):
        compo_dict[i]['terms'] = test_compo[i][which]
    for zuowen in compo_dict:
        if zuowen['terms']==[]:
            zuowen['terms'].append('无主题')

    valid = random.sample(compo_dict,int(np.floor(len(compo_dict)*valid_ratio)))
    test = []
    if iftest:
        test = random.sample(compo_dict,int(np.floor(len(compo_dict)*test_ratio)))
    train = [i for i in compo_dict if (i not in valid and i not in test)]

    with open('train.txt', 'w', encoding='utf-8') as f:
        for i in train:
            f.write(str(i))
            f.write('\n')
    with open('valid.txt', 'w', encoding='utf-8') as f:
        for i in valid:
            f.write(str(i))
            f.write('\n')
    with open('test.txt', 'w', encoding='utf-8') as f:
        for i in test:
            f.write(str(i))
            f.write('\n')
lastprocess(compo_dict, test_compo, 'Last10')
