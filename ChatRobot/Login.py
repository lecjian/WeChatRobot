#coding=utf8
import time
import random
import re
import os
import Data
import Tools

class Login:
    def __init__(self):
        self.main()

    def main(self):
        if self.get_uuid():
            self.get_qrcode()
            print '[INFO] Please use WeChat to scan the QR code .'
        else:
            print '[ERROR] Can\'t get uuid please retry...'

    def get_uuid(self):
        params = {
            'appid': 'wx782c26e4c19acffb',
            'fun': 'new',
            'lang': 'zh_CN',
            '_': int(time.time()) * 1000 + random.randint(1, 999),
        }
        result = Data.session.get(Data.url_get_uuid, params = params)
        result.encoding = Data.encoding
        regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
        data = re.search(regx, result.text)
        if data:
            code = data.group(1)
            Data.uuid = data.group(2)
            return code == Data.SUCCESS
        return False

    def get_qrcode(self):
        img_dir = os.path.join(Data.DATA_DIR, 'WXQR.jpg')
        result = Data.session.get(Data.url_get_qrcode + Data.uuid, stream=True)
        Tools.write_file(result.content, img_dir, 'wb')
        os.startfile(img_dir) # open image