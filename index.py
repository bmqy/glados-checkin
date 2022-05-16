# -*- coding: utf-8 -*-

import os
import requests
import json
import re

# Telegram私聊推送
tele_api_url = 'https://api.telegram.org'
tele_bot_token = os.environ.get('tele_bot_token')
tele_user_id = os.environ.get('tele_user_id')
# 填入glados账号对应cookie
cookie = os.environ["cookie"]
# 填入glados网站验证token
token = os.environ["token"]


def start():
    
    url= "https://glados.rocks/api/user/checkin"
    url2= "https://glados.rocks/api/user/status"
    origin = "https://glados.rocks"
    referer = "https://glados.rocks/console/checkin"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    payload={
        'token': token
    }
    checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
    state =  requests.get(url2,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
   # print(res)

    if 'message' in checkin.text:
        mess = checkin.json()['message']
        email = state.json()['data']['email']
        time = state.json()['data']['leftDays']
        time = time.split('.')[0]
        msg = (
            f"\n账号：{email}"
            f"\n提示：{mess}"
            f"\n余额：{time} 天后到期"
        )
        #print(time)
        tele_send(msg)
    else:
        tele_send('cookie过期')


def tele_send(msg: str):
    if tele_bot_token == '':
        return
    tele_url = f"{tele_api_url}/bot{tele_bot_token}/sendMessage"
    content = "\n".join([
        "签到站点：https://glados.rocks",
        "签到结果："+ str(msg)
    ])
    data = {
        'chat_id': tele_user_id,
        'parse_mode': "Markdown",
        'text': content
    }
    requests.post(tele_url, data=data)

def main_handler(event, context):
  return start()

if __name__ == '__main__':
    start()
