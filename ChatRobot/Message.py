import urllib
import re
import time
import os
import json
import Data
import Tools

class Message:
    def __init__(self, contactsClass):
        self.contacts = contactsClass
        self.sync_msg()
        
    def sync_msg(self):
        while True:
            try:
                code, selector = self.sync_check()
                if code == '0':
                    msg = self.get_msg()
                    if msg is not None:
                        self.analyze_msg(msg)
                    # print '[INFO] Have new message'
                elif code == '10101':
                    print '[INFO] Loginout on other client'
                time.sleep(10)
            except:
                print '[ERROR] Except in proc_msg'

    def sync_check(self):
        params = {
            'r': int(time.time()),
            'sid': Data.sid,
            'uin': Data.uin,
            'skey': Data.skey,
            'deviceid': Data.device_id,
            'synckey': Data.sync_key_str,
            '_': int(time.time()),
        }
        url = 'https://webpush.' + Data.host_base + '/cgi-bin/mmwebwx-bin/synccheck?' + urllib.urlencode(params)

        try:
            result = Data.session.get(url, timeout = 60)
            result.encoding = Data.encoding
            data = re.search(r'window.synccheck=\{retcode:"(\d+)",selector:"(\d+)"\}', result.text)
            return data.group(1), data.group(2)
        except:
            return -1, -1

    def get_msg(self):
        url = Data.url_base + '/webwxsync?sid=%s&skey=%s&lang=en_US&pass_ticket=%s' \
                              % (Data.sid, Data.skey, Data.pass_ticket)
        params = {
            'BaseRequest': Data.base_request,
            'SyncKey': Data.sync_key,
            'rr': ~int(time.time())
        }
        try:
            rsult = Data.session.post(url, data=json.dumps(params), timeout=60)
            rsult.encoding = Data.encoding
            dic = json.loads(rsult.text)
            if dic['BaseResponse']['Ret'] == 0:
                Data.sync_key = dic['SyncKey']
                Data.sync_key_str = '|'.join([str(keyVal['Key']) + '_' + str(keyVal['Val'])
                                              for keyVal in Data.sync_key['List']])
            
            if Data.DEBUG:
                Tools.write_file(json.dumps(dic), os.path.join(Data.TEMP_DIR, 'msg_dic.json'), 'w' )
            return dic
        except:
            return None

    def analyze_msg(self, dic):
        '''
        51 login init contact user name
        1  message
           location
                content: XXXXXX:<br/>/cgi-bin/mmwebwx-bin/webwxgetpubliclinkimg?url=xxx&msgid=XXXX97264734&pictype=location
        3  image
        34 voice msg
        42 recommend
        43 video msg
        47 user define emoji pic url in keyword 'cdnurl'
        49 share
        53 video call
        '''
        for msg in dic['AddMsgList']:
            msg_type = msg['MsgType']

            if msg_type == 1:
                msg_content = msg['Content']
                user_name = msg['FromUserName']
                name = self.contacts.get_name(user_name)
                if msg_content.find('=location') != -1:
                    index = msg_content.find(':')
                    msg_content = msg_content[:index]
                print '%s : %s'%(name, msg_content)

            elif msg_type == 3:
                print 'receive image'

            elif msg_type == 34:
                print 'receive voice msg'

            elif msg_type == 42:
                self.show_recommend(msg)

            elif msg_type == 43:
                print 'video msg'

            elif msg_type == 47:
                print 'emoji pic'

            elif msg_type == 49:
                self.show_share(msg)

            elif msg_type == 53:
                print 'video call'

    def show_recommend(self, msg):
        info = msg['RecommendInfo']
        print '[RecommendInfo]:'
        print '-NickName: %s' % info['NickName']
        print '-Alias: %s' % info['Alias']
        print '-Local: %s %s' % (info['Province'], info['City'])
        print '-Gender: %s' % ['unknown', 'male', 'female'][info['Sex']]

    def show_share(self, msg):
        print '[Share]:'
        print '-title: %s' % msg['FileName']
        print '-desc: '
        print '-link: %s' % msg['Url']
        print '-content: %s' % (msg.get('content')[:20] if msg.get('content') else "unknown")





    