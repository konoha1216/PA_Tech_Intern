import urllib.request as urllib2
import sys
import ssl

# client_id 为官网获取的AK， client_secret 为官网获取的SK
# client_id is the API Key, client_secret is the Secret Key
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【client_id】&client_secret=【client_secret】'
request = urllib2.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')

## you may need this step to eliminate the verification
context = ssl._create_unverified_context()

response = urllib2.urlopen(request, context=context)
content = response.read()
if (content):
    print(content)