#!/usr/bin/python
#-*-coding:utf-8-*-
import ConfigParser
import os
import sys
sys.path.append("..")
from jsondb.jsondb import *

class ConfigData:
    def __init__(self):
        self.db = JsonDbJetty()
        self.cfg = self.db.get_info('config', 'fname')

    def read_cfg(self, field, name):
        cf = ConfigParser.ConfigParser()
        cf.read(self.cfg)
        value= cf.get(field, name)
        return value

    def write_cfg(self, field, name, value):
        cf = ConfigParser.ConfigParser()
        cf.read(self.cfg)
        cf.set(field, name, value)
        f = open(self.cfg, "w")
        cf.write(f)
        f.close()
