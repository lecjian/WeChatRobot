#coding=utf8
import time
import random
import re
import os
import Data
import Tools
import xml.dom.minidom
import json

class Login:
    def __init__(self):
        self.main()

    def main(self):
        if self.get_uuid():
            self.get_qrcode()
            print '[INFO] Please use WeChat to scan the QR code .'

            result = self.login()
            if result != Data.SUCCESS:
                print '[ERROR] Login failed. failed code=%s' % (result,)
                Data.login_status = 'loginout'
                return

            if self.get_login_callback_info():
                print '[INFO] WeChat login succeed .'
            else:
                print '[ERROR] WeChat login failed .'
                self.status = 'loginout'
                return

            if self.login_init():
                print '[INFO] WeChat init succeed .'
            else:
                print '[INFO] WeChat init failed'
                self.status = 'loginout'
                return
            
            self.status_notify()
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

    def do_request(self, url):
        result = Data.session.get(url)
        result.encoding = Data.encoding
        data = re.search(r'window.code=(\d+);', result.text)
        code = data.group(1)
        return code, result.text

    def login(self):
        '''
        tip=1, wait for user scan the QR code 
               201: scaned
               408: timeout
        tip=0, wait for user confirmed login
               200: confirmed
        '''
        tip = 1
        retry_time = 10
        try_later_secs = 1
        while retry_time > 0:
            url = Data.url_login %(tip, Data.uuid, int(time.time()))
            code, data = self.do_request(url)

            if code == Data.SCANED: 
                print '[INFO] Please confirm to login.'
                tip = 0
            elif code == Data.SUCCESS:
                param = re.search(r'window.redirect_uri="(\S+?)";', data)
                redirect_uri = '%s&fun=new'%param.group(1)
                Data.redirect_uri = redirect_uri
                Data.url_base = redirect_uri[:redirect_uri.rfind('/')]
                temp_host = Data.url_base[8:]
                Data.host_base = temp_host[:temp_host.find("/")]
                return code
            elif code == Data.TIMEOUT:
                print '[ERROR] Login timeout, retry in %s secs later'%(try_later_secs)
                tip = 1
                retry_time -= 1
                time.sleep(try_later_secs)
            else:
                print '[ERROR] Login exception return code %s. retry in %s secs later'%(code, try_later_secs)
                tip = 1
                retry_time -= 1
                time.sleep(try_later_secs)
        return code
    
    def get_login_callback_info(self):
        '''callback login infomation'''
        if len(Data.redirect_uri) < 4:
            print '[ERROR] Login url error please try again'
            return False

        result = Data.session.get(Data.redirect_uri)
        result.encoding = 'utf-8'
        data = result.text
        doc = xml.dom.minidom.parseString(data)
        root = doc.documentElement
        
        for node in root.childNodes:
            if node.nodeName == 'skey':
                Data.skey = node.childNodes[0].data
            if node.nodeName == 'wxsid':
                Data.sid = node.childNodes[0].data
            if node.nodeName == 'wxuin':
                Data.uin = node.childNodes[0].data
            if node.nodeName == 'pass_ticket':
                Data.pass_ticket = node.childNodes[0].data
        if '' in (Data.skey, Data.sid, Data.uin, Data.pass_ticket):
            return False

        Data.base_request={
            'Uin':Data.uin,
            'Sid':Data.sid,
            'Skey':Data.skey,
            'DeviceID':Data.device_id,
        }
        return True

    def login_init(self):
        url = Data.url_base + '/webwxinit?r=%i&lang=en_US&pass_ticket=%s' % (int(time.time()), Data.pass_ticket)
        params = {'BaseRequest':Data.base_request}

        result = Data.session.post(url, data = json.dumps(params))
        result.encoding = Data.encoding
        dic = json.loads(result.text)
        Data.my_account = dic['User']
        Data.sync_key = dic['SyncKey']
        Data.sync_key_str = '|'.join([str(keyVal['Key']) + "_" + str(keyVal['Val']) for keyVal in Data.sync_key['List']])

        return dic['BaseResponse']['Ret'] == 0


    def status_notify(self):
        url = Data.url_base + '/webwxstatusnotify?lang=zh_CN&pass_ticket=%s' % Data.pass_ticket
        Data.base_request['Uin'] = int(Data.base_request['Uin'])
        params = {
            'BaseRequest': Data.base_request,
            "Code": 3,
            "FromUserName": Data.my_account['UserName'],
            "ToUserName": Data.my_account['UserName'],
            "ClientMsgId": int(time.time())
        }

        result = Data.session.post(url, data=json.dumps(params))
        result.encoding = Data.encoding
        dic = json.loads(result.text)
        return dic['BaseResponse']['Ret'] == 0
