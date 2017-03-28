#coding=utf8
'''
Data module
Used to store all the data
'''
import requests
import os
import random

# code
SUCCESS = '200'
SCANED = '201'
TIMEOUT = '408'

DEBUG = True

# encoding
encoding = 'utf-8'

# path
PROJ_DIR =os.path.join(os.getcwd(),'ChatRobot') 
DATA_DIR = os.path.join(PROJ_DIR,'Data')
TEMP_DIR = os.path.join(PROJ_DIR,'Temp')
IMG_DIR = os.path.join(DATA_DIR,'Image')
VID_DIR = os.path.join(DATA_DIR,'Video')
LOG_DIR = os.path.join(DATA_DIR,'Log')


# Login and request data
uuid = ''
login_status = ''
skey = None
sid = None
uin = None
pass_ticket = None
base_request = None
device_id = 'e' + repr(random.random())[2:17]

my_account = None
sync_key = None
sync_key_str = None

#network request uir and host 
session = session = requests.Session()
url_get_uuid = 'https://login.weixin.qq.com/jslogin'
url_get_qrcode = 'https://login.weixin.qq.com/qrcode/'
url_login = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s'
url_base = '' # https://wx.qq.com/cgi-bin/mmwebwx-bin
host_base = ''
redirect_uri = ''

