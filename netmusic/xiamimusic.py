#! -*- coding:utf-8 -*-


import json
import requests
from song import Song
from bs4 import BeautifulSoup
from config import XIAMI_USERNAME, XIAMI_PASSWORD



class XiamiMusic(object):


    def __init__(self, username, password):
        self.username = username
        self.password = password
    
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.xiami.com',
            'Referer': 'http://www.xiami.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
        }
        self.cookies = {}
    
    def _request(self, method, action, data = None):
        if method == 'POST':
            conn = requests.post(action, data = data, headers = self.header, cookies = self.cookies)
        if method == 'GET':
            conn = requests.get(action, params = data, headers = self.header, cookies = self.cookies)
        conn.ending = 'utf-8'
        return conn
    


    def login(self):
        #action = 'http://www.xiami.com/web/login/'
        #data = {
        #    'email': self.username,
        #    'password': self.password,
        #    'remember': 1,
        #    'LoginButton': '登录'
        #}
        
        action = 'http://login.xiami.com/member/login'
        data = {
            'email' : self.username,
            'password' : self.password,
            'submit' : '登 录',
            'from' : 'web'
        }

        conn = self._request('POST', action, data)
        self.cookies = conn.cookies
        
        result = conn.json()
        self.userid = result.get('data').get('user_id')



    def _parse_collect_song(self, response):
        results = []
        soup = BeautifulSoup(response, 'lxml')
        for td in soup.find_all('td', attrs = {'class' : 'song_name'}):
            items = td.find_all('a')
            song_name = items[0]['title'].encode('utf-8')
            song_artist = (items[1]['title'] if len(items) == 2 else items[2]['title']).encode('utf-8')
            results.append(Song(name = song_name, artist = song_artist))
        return results
            
    def get_collect_song(self):
        action = 'http://www.xiami.com/space/lib-song/u/%s/page/' % self.userid
        
        songs = []
        page = 1
        while True:
            res = self._parse_collect_song(self._request('GET', action + str(page)).text)
            if not res:
                break
            songs.extend(res)
            page = page + 1
        #self._write_to_file('\n'.join(str(item) for item in songs), 'xiami_clooect_song')
        return songs
    
    def _parse_collect_artist(self, response):
        results = []
        soup = BeautifulSoup(response, 'lxml')
        for p in soup.find_all('p', attrs = {'class' : 'name'}):
            artist = p.find('a')['title'].encode('utf-8')
            results.append(artist)
        return results

    def get_collect_artist(self):
        action = 'http://www.xiami.com/space/lib-artist/u/%s/page/' % self.userid
        
        artists = []
        page = 1
        while True:
            res = self._parse_collect_artist(self._request('GET', action + str(page)).text)
            if not res:
                break
            artists.extend(res)
            page = page + 1

        self._write_to_file('\n'.join(artists), 'xiami_collect_artists')
        return artists
        
    def _parse_collect_album(self, response):
        results = []
        soup = BeautifulSoup(response, 'lxml')
        for p in soup.find_all('div', attrs = {'class' : 'name'}):
            artist = p.find('a')['title'].encode('utf-8')
            results.append(artist)
        return results

    def get_collect_album(self):
        action = 'http://www.xiami.com/space/lib-album/u/%s/page/' % self.userid

        albums = []
        page = 1
        while True:
            res = self._parse_collect_album(self._request('GET', action + str(page)).text)
            if not res:
                break
            albums.extend(res)
            page = page + 1

        self._write_to_file('\n'.join(albums), 'xiami_collect_albums')
        return albums

    def _write_to_file(self, content, filename):
        with open(filename, 'wb') as myfile:
            if isinstance(content, unicode):
                content = content.encode('utf-8')
            myfile.write(content)

if __name__ == '__main__':
    api = XiamiMusic(XIAMI_USERNAME, XIAMI_PASSWORD)
    api.login()
#   api.get_collect_song()
#   api.get_collect_artist()
    api.get_collect_album()
