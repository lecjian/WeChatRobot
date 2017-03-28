#coding=utf8
import time
import os
import json
import Data
import Tools

class Contacts:
    def __init__(self):
        self.get_contacts()

    def get_contacts(self):
        '''
        Access to all accounts of the current account 
        including contacts, public numbers, group chat, special account
        '''
        url = Data.url_base + '/webwxgetcontact?pass_ticket=%s&skey=%s&r=%s'\
                % (Data.pass_ticket, Data.skey, int(time.time()))
        try:
            result = Data.session.post(url, data='{}')
        except Exception as e:
            print '[ERROR] Get contacts fail'
            return False
        result.encoding = Data.encoding
        if Data.DEBUG:
            path = os.path.join(Data.TEMP_DIR, 'contacts.json')
            Tools.write_file(result.text.encode('utf-8'), path, 'w')
