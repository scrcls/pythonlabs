#! -*- coding:utf-8 -*-


import json

if __name__ == '__main__':
    with open('test', 'rb') as myfile:
        content = myfile.read()
    content = json.loads(content)    
    with open('testresult', 'wb') as myfile:
        myfile.write(json.dumps(content, ensure_ascii = False).encode('utf-8'))
