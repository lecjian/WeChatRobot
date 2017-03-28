import urllib
import re
import time
import os
import json
import Data
import Tools

class Message:
    def __init__(self):
        self.sync_msg()

    def sync_msg(self):
        while True:
            try:
                code, selector = self.sync_check()
                if code == '0':
                    if selector == '2':
                        self.get_msg()
                    print '[INFO] Have new message'
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
    
