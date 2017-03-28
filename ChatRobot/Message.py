import urllib
import re
import time
import Data

class Message:
    def __init__(self):
        self.get_msg()

    def get_msg(self):
        while True:
            try:
                code, selector = self.sync_check()
                if code == '0':
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
    
