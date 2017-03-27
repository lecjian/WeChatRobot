#coding=utf8
'''
Data module
Used to store all the data
'''
import requests

# code
SUCCESS = '200'
SCANED = '201'
TIMEOUT = '408'

# encoding
encoding = 'utf-8'

#network request uir and host 
session = session = requests.Session()
get_uuid_url = 'https://login.weixin.qq.com/jslogin'
base_url = '' # https://wx.qq.com/cgi-bin/mmwebwx-bin

# Login and request data
uuid = None