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
        except:
            print '[ERROR] Get contacts fail'
            return False
        result.encoding = Data.encoding
        if Data.DEBUG:
            Tools.write_file(result.text.encode('utf-8'), Data.TEMP_DIR, 'contacts.json', 'w')

        self.init_contacts_data(result.text)

    def init_contacts_data(self, data):
        dic = json.loads(data)
        contacts_info = dic['MemberList']
        for contact in contacts_info:
            if contact['VerifyFlag'] == 0: 
                if contact['UserName'].find('@@') != -1: #group
                    Data.group_list.append(contact)
                else: #friends
                    Data.friend_list.append(contact)
            else:  #public
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

    def get_contact_name(self, user_name, lists):
        for contact in lists:
            if user_name == contact['UserName']:
                return contact['RemarkName'] if contact['RemarkName'] else contact['NickName']
        return None

    def get_name(self, user_name):
        if self.is_friend(user_name):
            return self.get_contact_name(user_name, Data.friend_list)
        elif self.is_group(user_name):
            return self.get_contact_name(user_name, Data.group_list)
        elif self.is_pubilc(user_name):
            return self.get_contact_name(user_name, Data.public_list)
        return 'unknow'

    def get_user_id(self, name):
        if name == '':
            return None
        for contact in Data.friend_list:
            if 'RemarkName' in contact and contact['RemarkName'] == name:
                return contact['UserName']
            if 'NickName' in contact and contact['NickName'] == name:
                return contact['UserName']
        for group in Data.group_list:
            if 'RemarkName' in group and group['RemarkName'] == name:
                return group['UserName']
            if 'NickName' in group and group['NickName'] == name:
                return group['UserName']
        return None

    def set_remarkname(self, user_id, remarkname):
        url = Data + '/webwxoplog?lang=zh_CN&pass_ticket=%s'%Data.pass_ticket
        params = {
            'BaseRequest': Data.base_request,
            'CmdId': 2,
            'RemarkName': remarkname,
            'UserName': user_id
        }
        try:
            result = Data.session.post(url, data = json.dumps(params), timeout = 60)
            result.encoding = Data.encoding
            dic = json.loads(result.text)
            return dic['BaseResponse']['ErrMsg']
        except:
            return None

    