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
        including contacts, public numbers, group chat
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

        self.init_contacts_data(result.text)

    def init_contacts_data(self, data):
        dic = json.loads(data)
        contacts_info = dic['MemberList']
        for contact in contacts_info:
            if contact['Sex'] != 0: #friends
                Data.friend_list.append(contact)
            elif contact['UserName'].find('@@') != -1: #group
                Data.group_list.append(contact)
            elif contact['VerifyFlag'] != 0: #public
                Data.public_list.append(contact)

    def is_friend(self, user_name):
        for contact in Data.friend_list:
            if user_name == contact['UserName']:
                return True
        return False

    def is_group(self, user_name):
        for contact in Data.group_list:
            if user_name == contact['UserName']:
                return True
        return False

    def is_pubilc(self, user_name):
        for contact in Data.public_list:
            if user_name == contact['UserName']:
                return True
        return False

    def get_contact_name(self, user_name, list):
        for contact in Data.friend_list:
            if user_name == contact['UserName']:
                return contact['RemarkName'] if contact['RemarkName'] else contact['NickName']
        return None

    def get_name(self, user_name):
        if self.is_friend:
            return self.get_contact_name(user_name, Data.friend_list)
        elif self.is_group:
            return self.get_contact_name(user_name, Data.group_list)
        elif self.is_pubilc:
            return self.get_contact_name(user_name, Data.public_list)
        return 'unknow'

    