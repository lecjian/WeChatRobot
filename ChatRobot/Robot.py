#coding=utf8
import json
import Data

def load_config():
    try:
        with open('%s\config.json'%Data.PROJ_DIR) as f:
            data = json.load(f)
            Data.tuling_api = data['Api']
            Data.tuling_key = data['Key']
    except:
        print '[ERROR] You need to have a correct config.json file'

def auto_reply(user_id, msg):
    if Data.tuling_api and Data.tuling_key:
        user_id = user_id.replace('@', '')[:30]
        body = {
            'key':Data.tuling_key,
            'info':msg.encode('utf8'),
            'userid':user_id
        }
        result = Data.session.post(Data.tuling_api, data = body)
        data = json.loads(result.text)
        return get_response(data)
    else:
        print '[ERROR] Robot api or key null'
        

def get_response(data):
    if not data['code'] in (100000, 200000, 302000, 308000, 313000, 314000):
        if data['code'] == 400004: 
            return None
        raise Exception('code: %s'%data['code'])
    elif data['code'] == 100000: # Text
        return data['text'].replace('<br>','\n')
    elif data['code'] == 200000: # Url
        return data['text'].replace('<br>','\n'), data['url']
    elif data['code'] == 313000: # Child Song
        return data['text'].replace('<br>','\n')
    elif data['code'] == 314000: # poem
        return data['text'].replace('<br>','\n')

def auto_switch(user_id, msg):
    if not Data.LOAD_CONFIG:
        load_config()
    stop_cmd = [u'退出', u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
    start_cmd = [u'出来', u'启动', u'工作', u'开启',  u'机器人']

    is_start = True if user_id in Data.start_robot_user_list else False
    is_chated = True if user_id in Data.user_haved_chat_list else False

    if is_start:
        for cmd in stop_cmd:
            if cmd == msg:
                Data.start_robot_user_list.remove(user_id)
                return False, u'机器人已关闭！'
        return True, None
    else:
        if is_chated == False:
            Data.user_haved_chat_list.append(user_id)
            return False, u'您好，主人现在有事不在\n可以留言或开启聊天模式。\n回复“出来”,“启动”,“机器人”开启\n回复“关闭”,“退下”,“休息”关闭\n机器人模式可以随时开启和关闭哦'
        for cmd in start_cmd:
            if cmd == msg:
                Data.start_robot_user_list.append(user_id)
                return False, u'机器人已开启！和机器人聊天吧'
    return False, None
                    

