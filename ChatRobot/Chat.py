from Login import Login
from Contacts import Contacts
from Message import Message
from Group import Group

if __name__ == '__main__':
    login = Login()
    contacts = Contacts()
    group = Group()
    message = Message(contacts)
    