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
    load_config()
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
    stop_cmd = [u'退出', u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
    start_cmd = [u'出来', u'启动', u'工作', u'开启',  u'机器人']
    if Data.robot_switch:
        for cmd in stop_cmd:
            if cmd == msg:
                Data.robot_switch = False
                return u'机器人已关闭！'
        content = auto_reply(user_id, msg)
        return content
    else:
        if Data.first_chat:
            Data.first_chat = False
            return u'您好，我现在有事不在\n可以留言或开启机器人聊天模式。\n回复“出来”,“启动”,“机器人”开启\n回复“关闭”,“退下”,“休息”关闭\n机器人模式可以随时开启和关闭哦'
        for cmd in start_cmd:
            if cmd == msg:
                Data.robot_switch = True
                return u'机器人已开启！和机器人聊天吧'
    return None
                    

