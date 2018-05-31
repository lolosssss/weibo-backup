# -*- coding: utf-8 -*-

from WeiboClient import WeiboClient

APP_SECRET = "xxx"
APP_KEY = "xxx"
CODE = "xxx"
ACCESS_TOKEN = "xxx"
UID = "xxx"
REDIRECT_URI = "http://api.weibo.com/oauth2/default.html"

def run():
    weibo_client = WeiboClient(APP_KEY, APP_SECRET, REDIRECT_URI)
    response = weibo_client.request_user_timeline(UID, ACCESS_TOKEN)
    statuses = response['statuses']
    length = len(statuses)
    for i in range(0, length):
        print(statuses[i]['text'])

if __name__ == "__main__":
    run()
