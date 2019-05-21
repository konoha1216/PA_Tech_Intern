# coding:utf-8
import urllib
import urllib.request as urllib2
import base64
import ssl


access_token = "Your access_token from the last step"

url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + access_token

# 二进制方式打开图文件
# open the image file in binary format
f = open(r'test2.jpg', 'rb')
# 参数image：图像base64编码
# parameter image: the image's base64 encoding
img = base64.b64encode(f.read())
params = {"image": img}
params = urllib.parse.urlencode(params).encode('utf-8')

request = urllib2.Request(url, data = params)
request.add_header('Content-Type', 'application/x-www-form-urlencoded')
context = ssl._create_unverified_context()
response = urllib2.urlopen(request, context=context)
content = response.read().decode('utf-8')
if (content):
    print('correct')

## print the recognized words to a text in the local directory
mydict = eval(content)
with open('result.txt','w') as f:
    for thing in mydict['words_result']:
        f.write(thing['words'])
        f.write('\n')