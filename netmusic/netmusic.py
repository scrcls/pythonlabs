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
	
	def request(self, method, action, data):
		if method == 'GET':
			connection = requests.get(action, params = data, headers = self.header, cookies = self.cookies)
		if method == 'POST':
			connection = requests.post(action, data = data, headers = self.header, cookies = self.cookies)
		connection.encoding = 'utf-8'
		return connection

	def login(self, username, password):

		action = 'http://music.163.com/api/login/'
		data = {
    		'username': username,
    		'password': hashlib.md5(password).hexdigest(),
    		'rememberLogin': 'true',
    	}
		ret = self.request('POST', action, data)
		self.cookies = ret.cookies
		# ';'.join([key + '=' + self.cookies[key] for key in dict(self.cookies).keys()])
		return ret

	def getUserList(self, userid):
		action = 'http://music.163.com/api/user/playlist/'
		data = {
			'limit': 1001,
			'offset': 0,
			'uid': userid,
		}
		return self.request('GET', action, data)


	def creatList(self, listname):

		action = 'http://music.163.com/api/playlist/create/'
		data = {
			'name': listname,
			'uid': '6850177',
		}
		connection = requests.post(action, data = data, headers = self.header, cookies = self.cookies)
		print connection.text

	def deleteList(self, listid):
		action = 'http://music.163.com/api/playlist/delete'
		data = {
			'pid': listid,
		}
		ret = self.request('GET', action, data)
		print ret


if __name__ == '__main__':
	api = NetMusicApi()
	api.login(NETMUSIC_USERNAME, NETMUSIC_PASSWORD)
	# print user['account']['id']
	api.creatList('test10')
	# api.deleteList('56479233')

	# playlists = api.getUserList('6850177')['playlist']
	# for playlist in playlists:
	# 	print playlist['name'], playlist['id']



