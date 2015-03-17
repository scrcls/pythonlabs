# -*- coding:utf-8 -*-


import requests
import hashlib
import json
from config import NETMUSIC_PASSWORD, NETMUSIC_USERNAME

class NetMusicApi:

    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/my/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
        }
        self.cookies = {}
        

    def _request(self, method, action, data):
        if method == 'GET':
            connection = requests.get(action, params = data, headers = self.header, cookies = self.cookies)
        if method == 'POST':
            connection = requests.post(action, data = data, headers = self.header, cookies = self.cookies)
        connection.encoding = 'utf-8'
        return connection

    def _neteast_passport(self, username, password):
        action = 'https://reg.163.com/logins.jsp'
        data = {
            'username':username,
            'password':password
        }
        ret = self._request('POST', action, data)
        self.cookies = ret.cookies
        
    
    def login(self, username, password):
        action = 'http://music.163.com/api/login/'
        data = {
            'username': username,
            'password': hashlib.md5(password).hexdigest(),
            'rememberLogin': 'true',
        }
        conn = self._request('POST', action, data)
        self.cookies = conn.cookies
        
        result = conn.json()
        self.userid = result.get('account').get('id')
        return result.get('code') == 200
    
    def create_list(self, listname):
        action = 'http://music.163.com/api/playlist/create?csrf_token=' + self.cookies['__csrf']
        print action
        data = {
            'name': listname,
        }
        conn = self._request('POST', action, data)
        result = conn.json()
        return result.get('code') == 200
        
    def delete_list(self, listid):
        action = 'http://music.163.com/api/playlist/delete'
        data = {
            'pid': listid,
            'csrf_token': self.cookies['__csrf']
        }
        conn = self._request('GET', action, data)
        result = conn.json()
        return result.get('code') == 200

    def get_user_list(self):
        action = 'http://music.163.com/api/user/playlist/'
        data = {
            'limit': 1001,
            'offset': 0,
            'uid': self.userid,
        }
        conn = self._request('GET', action, data)
        return conn.json()
    
    def get_listid(self, listname):
        userlist = self.get_user_list()
        for item in userlist.get('playlist'):
            if item.get('name') == listname.decode('utf-8'):
                return item.get('id')
        return None

if __name__ == '__main__':
    api = NetMusicApi()
    api.login(NETMUSIC_USERNAME, NETMUSIC_PASSWORD)
    testid = api.listid('test1')
    print testid
    print api.delete_list(testid)
