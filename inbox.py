#!/usr/bin/python
#-*-coding:utf-8-*-
import os
import sys
import string
import socket
import poplib
import ConfigParser

from time import sleep
from blog_handle import *
from jsondb.jsondb import *
from config.config import *
from blog_module import BlogJetty

class Input:
    def __init__(self):
        print 'bloginput'

class EmailInput(Input):
    def __init__(self):
        print 'emailinput'

class Pop3Input(EmailInput):
    def __init__(self):
        print 'pop3input'
        self.server = None

    def login(self):
        self.server = None
        db = JsonDbJetty()
        email_rec = db.get_info('email', 'email')
        email_pwd = db.get_info('email', 'password')
        email_pop3 = db.get_info('email', 'server')
        try:
            self.server = poplib.POP3(email_pop3,timeout=5)
            self.server.user(email_rec)
            self.server.pass_(email_pwd)
            print(self.server.getwelcome())
            self.index, self.size = self.server.stat()
        except socket.error, err:
            return 1
        except poplib.error_proto:
            return 2
        else:
            print 'welcome email system'
        return 0

    def get_db_index(self):
        cfg = ConfigData()
        return cfg.read_cfg('db','index')

    def set_db_index(self, index):
        cfg = ConfigData()
        cfg.write_cfg('db','index', index)

    def get_server(self):
        return self.server

    def get_index(self):
        return self.index
