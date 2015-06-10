#! /usr/bin/python
#! -*- coding:utf-8 -*-


import requests
import base64

import config

################################################################################
#imagetype = 1 : 使用base64对图像文件进行处理
#                目前仅支持使用jpg格式

################################################################################

def open_img_base64(img_file):
    with open(img_file, 'rb') as my_file:
        img_data = my_file.read()
    return base64.b64encode(img_data)


def ocr_img(img_file):

    ocr_url = 'http://apis.baidu.com/apistore/idlocr/ocr'
    ocr_header = {
            'apikey' : config.apikey,
            'Content-Type' : 'application/x-www-form-urlencoded',
    }

    ocr_data = dict(fromdevice = 'pc',
                    clientip = '10.10.10.0',
                    detecttype = 'LocateRecognize',
                    languagetype = 'CHN_ENG',
                    imagetype = '1',
                    image = open_img_base64(img_file),
                    )

    conn = requests.post(ocr_url, data = ocr_data, headers = ocr_header)
    #print conn.status_code
    #print conn.json()['errMsg']
    if conn.json()['errNum'] != '0':
        return None
    return conn.json()['retData'][0]['word']


if __name__ =='__main__':
    print ocr_img('yzm.jpg')
