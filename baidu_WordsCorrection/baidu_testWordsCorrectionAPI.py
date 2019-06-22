from aip import AipNlp
from preprocessing import processing
import time
app_id = '16605938'
api_key = 'wWjS5w7z5mP1AxZKI2sx6q7s'
secret_key = 'AGSEARrY9qBGMLbBylGDiL75ilK17B2u'

client = AipNlp(app_id, api_key, secret_key)
# text_list = ['欢迎来到王者农药',
#              '我暑假在伤害实习',
#              '今天晚上去舰身吗？',
#              '你说我这句话里又没有错误',
#              '今年八月底就要回洛山鸡了',
#              '胡人总冠军！',
#              '贸易战会不会影像中美关系呢',
#              '不想遍了，直接从网上找错误的栗子吧',
#              '我去买个句子，你就在此地不要离开',
#              '夏天到了，我想吃水密桃',
#              '晚上睡觉开空调怕是要感帽哟',
#              '618想买一套键鼠啊',
#              '这个连湖人总瓜君都检测不出来的嘛',
#              '实习的时候坐在我旁边的是白老湿',
#              '等啊等，忠于等到了。',
#              '在最近的项目中，我们采用了pycorrector的九错逻辑，如下图所示',
#              '使用预言模型计算句子或序列的合理性',
#              '针对医学数据训练出来的，基于编辑举例，可自行训练',
#              '妹妹走之前还得给他再个新电脑',
#              '项目做的比较急，吊唁的package不多，如果有更好的方案，求告知，谢谢啦！'
#              ]
# print(len(text_list))
# for text in text_list:
#     print(client.ecnet(text))

# text = '急烈的比赛即将开始，运动员在跑道上紧张地做着准备动作。'
# print(client.ecnet(text))

error_list, correct_list, correction = processing('bcmi')
# print(error_list)
# print(correct_list)
# print(correction)

with open('bcmi_errorList.txt', 'w') as f:
    for sent in error_list:
        f.write(sent)
        f.write('\n')
with open('bcmi_correctList.txt', 'w') as f:
    for sent in correct_list:
        f.write(sent)
        f.write('\n')
with open('bcmi_Correction.txt', 'w') as f:
    for sent in correction:
        f.write(str(sent))
        f.write('\n')
baidu = []
flag = 0
num = 0
for text in error_list:
    jiucuo = client.ecnet(text)['item']['correct_query']
    baidu.append(jiucuo)
    if jiucuo == correct_list[flag]:
        num+=1
    print("wrong sent: ", text)
    print("correct sent: ", correct_list[flag])
    print("jiucuo sent: ", jiucuo)
    flag += 1
    print("total sent: ", flag, ", right correction: ", num, ", current precision: ", num/flag)
    print()
    with open("bcmi_baidu.txt", 'a') as f:
        f.write(jiucuo)
        f.write('\n')
    f.close()
    time.sleep(12)
