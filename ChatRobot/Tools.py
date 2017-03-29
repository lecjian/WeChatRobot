#coding=utf8
import re
import os
import Data


def write_file(stream_data, file_dir, mode):
    with open(file_dir, mode) as f:
        f.write(stream_data)

def get_user_head_icon(user_id, group_id = None):
    if group_id == None:
        url = Data.url_base + '/webwxgeticon?username=%s&skey=%s' % (user_id, Data.skey)
    else:
        url = Data.url_base + '/webwxgeticon?username=%s&skey=%s&chatroomid=%s' % (
            user_id, Data.skey, Data.encry_chat_room_id_list[group_id])
    result = Data.session.get(url)

    file_name = 'icon_' + user_id + '.jpg'
    write_file(result.content, os.path.join(Data.USER_ICON_DIR, file_name), 'wb')
    return file_name

def get_group_head_icon(group_id):
    url = Data.url_base + '/webwxgetheadimg?username=%s&skey=%s' % (group_id, Data.skey)
    result = Data.session.get(url)

    file_name = 'icon_' + group_id + '.jpg'
    write_file(result.content, os.path.join(Data.GROUP_ICON_DIR, file_name), 'wb')
    return file_name

def get_msg_img(msg_id):
    url = Data.url_base + '/webwxgetmsgimg?MsgID=%s&skey=%s' % (msg_id, Data.skey)
    result = Data.session.get(url)

    file_name = 'img_' + msg_id + '.jpg'
    write_file(result.content, os.path.join(Data.IMG_DIR, file_name), 'wb')
    return file_name

def get_voice(msg_id):
    url =  Data.url_base + '/webwxgetvoice?msgid=%s&skey=%s' % (msg_id, Data.skey)
    result = Data.session.get(url)

    file_name = 'voice_' + msg_id + '.mp3'
    write_file(result.content, os.path.join(Data.VOI_DIR, file_name), 'wb')
    return file_name

def get_video(msg_id):
    url = self.base_uri + '/webwxgetvideo?msgid=%s&skey=%s' % (msg_id, Data.skey)
    headers = {'Range': 'bytes=0-'}
    result = Data.session.get(url, headers = headers)

    file_name = 'video_' + msg_id + '.mp4'
    write_file(result.content, os.path.join(Data.VID_DIR, file_name), 'wb')
    return file_name
