#! -*- coding:utf-8 -*-

import json

class BookmarkOrder(object):

    def __init__(self, filename):
        self.filename = filename

    def _read_from_file(self):
        with open(self.filename, 'rb') as myfile:
            self.filecontent = myfile.read()
        self.filecontent = json.loads(self.filecontent)

    def _write_to_file(self, filename = None):
        writefile = self.filename
        if filename:
            writefile = filename

        with open(writefile, 'wb') as myfile:
            myfile.write(json.dumps(self.filecontent).decode('gbk').encode('utf-8'))
    
    def get_child(self, jsondata, name):
        if not jsondata.get('children'):
            return None
        if not isinstance(jsondata['children'], list):
            return
        for item in jsondata['children']:
            if item['type'] == u'folder' and item['name'] == name.decode('utf-8'):
                return item
        return None

    def get_folder(self, names):
        names = names.split('-')

        folder = self.filecontent['roots']['bookmark_bar']
        for name in names:
            folder = self.get_child(folder, name)
            if not folder:
                return None
        return folder

    def order_by_date(self, reverse = False):
        
        data = self.get_folder('收藏夹-游戏')
        #for item in data['children']:
        #    print item['name']
        data['children'].reverse()



if __name__ == '__main__':
    orders = BookmarkOrder('Bookmarks')
    orders._read_from_file()
    orders.order_by_date()
    orders._write_to_file('book')
