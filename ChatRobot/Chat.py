from Login import Login
from Contacts import Contacts
from Message import Message
from Group import Group
import Data
import Tools

def get_data():
    for friend in Data.friend_list:
        Tools.get_user_head_icon(friend['UserName'])

    for group in Data.group_list:
        Tools.get_group_head_icon(group['UserName'])
        for member in group['MemberList']:
            Tools.get_user_head_icon(member['UserName', group['UserName']])

if __name__ == '__main__':
    login = Login()
    contacts = Contacts()
    group = Group()
    get_data()
    message = Message(contacts)


    