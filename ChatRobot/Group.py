import json
import os
import time
import Data
import Tools

class Group:
    def __init__(self):
        self.get_groups_members()
    
    def get_groups_members(self):
        url = Data.url_base + '/webwxbatchgetcontact?type=ex&r=%s&pass_ticket=%s' % (int(time.time()), Data.pass_ticket)
        params = {
            'BaseRequest': Data.base_request,
            "Count": len(Data.group_list),
            "List": [{"UserName": group['UserName'], "EncryChatRoomId": ""} for group in Data.group_list]
        }
        result = Data.session.post(url, data = json.dumps(params))
        result.encoding = Data.encoding
        dic = json.loads(result.text)
        for group in dic['ContactList']:
            group_id = group['UserName']
            members = group['MemberList']
            chat_room = group['EncryChatRoomId']
            Data.group_members[group_id] = members
            Data.encry_chat_room_id_list[group_id] = chat_room

        if Data.DEBUG:
            Tools.write_file(json.dumps(Data.group_members), os.path.join(Data.TEMP_DIR, 'group_members.json'), 'wb')

    def get_uid_by_name(self, group_name):
        for group in Data.group_list:
            if group['NickName'] == group_name:
                return group['UserName']
        return None

    def get_name_by_uid(self, uid):
        for group in Data.group_list:
            if group['UserName'] == uid:
                return group['NickName']
        return None

    def add_friend_to_group(self, uid, group_name):
        '''Add friends to group chat'''
        group_id = self.get_uid_by_name(group_name)
        if group_id is None: return False

        for group_user in Data.group_members[group_id]:
            if group_user['UserName'] == uid:
                return True #user in group

        group_num = len(Data.group_members[group_id])
        if group_num <= 100:
            url = Data.url_base + '/webwxupdatechatroom?fun=addmember&pass_ticket=%s' % Data.pass_ticket
            params ={
                "AddMemberList": uid,
                "ChatRoomName": group_id,
                "BaseRequest": Data.base_request
            }
        else:
            url = Data.url_base + '/webwxupdatechatroom?fun=invitemember'
            params ={
                "InviteMemberList": uid,
                "ChatRoomName": group_id,
                "BaseRequest": Data.base_request
            }
        headers = {'content-type': 'application/json; charset=UTF-8'}
        data = json.dumps(params, ensure_ascii = False).encode('utf8')
        try:
            result = Data.session.post(url, data = data, headers = headers)
        except (ConnectionError, ReadTimeout):
            return False
        dic = result.json()
        return dic['BaseResponse']['Ret'] == 0

    def invite_friend_to_group(self,uid,group_name):
        group_id = self.get_uid_by_name(group_name)
        if group_id is None: return False

        for group_user in Data.group_members[group_id]:
            if group_user['UserName'] == uid:
                return True #user in group

        url = Data.url_base + '/webwxupdatechatroom?fun=invitemember&pass_ticket=%s' % Data.pass_ticket
        params = {
            "InviteMemberList": uid,
            "ChatRoomName": group_id,
            "BaseRequest": Data.base_request
        }
        headers = {'content-type': 'application/json; charset=UTF-8'}
        data = json.dumps(params, ensure_ascii = False).encode('utf8')
        try:
            result = Data.session.post(url, data = data, headers = headers)
        except (ConnectionError, ReadTimeout):
            return False
        dic = result.json()
        return dic['BaseResponse']['Ret'] == 0

    def delete_user_from_group(self, user_name, group_id):
        user_id = None
        for user in Data.group_members[group_id]:
            if user['NickName'] == user_name:
                user_id = user['UserName']
        if user_id == None:
            return False
        url = Data.url_base + '/webwxupdatechatroom?fun=delmember&pass_ticket=%s' % Data.pass_ticket
        params ={
            "DelMemberList": user_id,
            "ChatRoomName": group_id,
            "BaseRequest": Data.base_request
        }
        headers = {'content-type': 'application/json; charset=UTF-8'}
        data = json.dumps(params, ensure_ascii = False).encode('utf8')
        try:
            result = Data.session.post(url, data = data, headers = headers)
        except (ConnectionError, ReadTimeout):
            return False
        dic = result.json()
        return dic['BaseResponse']['Ret'] == 0

    def set_group_name(self, group_id, group_name):
        url = Data.url_base + '/webwxupdatechatroom?fun=modtopic&pass_ticket=%s' % Data.pass_ticket
        params ={
            "NewTopic": group_name,
            "ChatRoomName": group_id,
            "BaseRequest": Data.base_request
        }
        headers = {'content-type': 'application/json; charset=UTF-8'}
        data = json.dumps(params, ensure_ascii = False).encode('utf8')
        try:
            result = Data.session.post(url, data = data, headers = headers)
        except (ConnectionError, ReadTimeout):
            return False
        dic = result.json()
        return dic['BaseResponse']['Ret'] == 0



