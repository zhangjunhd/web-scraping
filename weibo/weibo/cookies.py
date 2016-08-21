# -*- coding: utf-8 -*-
import json
import base64
import requests
from project_cfg import project_config


def get_cookies(weibo):
    """ 获取Cookies """
    cookie_list = []
    login_url = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    for elem in weibo:
        account = elem['id']
        password = elem['pwd']
        username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
        post_data = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": username,
            "service": "sso",
            "sp": password,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }
        session = requests.Session()
        r = session.post(login_url, data=post_data)
        json_str = r.content.decode('gbk')
        info = json.loads(json_str)
        if info["retcode"] == "0":
            print "Get Cookie Success!( Account:%s )" % account
            cookie = session.cookies.get_dict()
            cookie_list.append(cookie)
        else:
            print "Failed!( Reason:%s )" % info['reason']
    return cookie_list

cookies = get_cookies(project_config.get_cookies())
print "Get Cookies Finish!( Num:%d)" % len(cookies)

