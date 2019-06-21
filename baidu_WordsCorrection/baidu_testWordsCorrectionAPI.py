from aip import AipNlp
app_id = '16555096'
api_key = 'TB1j4tIHXIl9758TKwWVUHw9'
secret_key = 'kLmwYBh3keq7MoNpYZNemlT0rhTy7gVs'

client = AipNlp(app_id, api_key, secret_key)
text_list = ['欢迎来到王者农药',
             '我暑假在伤害实习',
             '今天晚上去舰身吗？',
             '你说我这句话里又没有错误',
             '今年八月底就要回洛山鸡了',
             '胡人总冠军！',
             '贸易战会不会影像中美关系呢',
             '不想遍了，直接从网上找错误的栗子吧',
             '我去买个句子，你就在此地不要离开',
             '夏天到了，我想吃水密桃',
             '晚上睡觉开空调怕是要感帽哟',
             '618想买一套键鼠啊',
             '这个连湖人总瓜君都检测不出来的嘛',
             '实习的时候坐在我旁边的是白老湿',
             '等啊等，忠于等到了。',
             '在最近的项目中，我们采用了pycorrector的九错逻辑，如下图所示',
             '使用预言模型计算句子或序列的合理性',
             '针对医学数据训练出来的，基于编辑举例，可自行训练',
             '妹妹走之前还得给他再个新电脑',
             '项目做的比较急，吊唁的package不多，如果有更好的方案，求告知，谢谢啦！'
             ]
print(len(text_list))
for text in text_list:
    print(client.ecnet(text))
