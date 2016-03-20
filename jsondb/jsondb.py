#!/usr/bin/python
import json
import os
class JsonDb:
    def __init__(self):
        self.cxt = None
        self.dict = None
        self.json_file = '/root/12/db.json'
        self.fp = None

    def open(self):
        self.fp = open(self.json_file)

    def read(self):
        self.cxt = self.fp.read()
        self.dict = json.loads(self.cxt)

    def get_dict(self):
        return self.dict

    def close(self):
        self.fp.close()

class JsonDbJetty(JsonDb):
    def __init__(self):
        JsonDb.__init__(self)

    def get_info(self, info, l1, l2=None):
        JsonDb.open(self)
        JsonDb.read(self)
        cxt = JsonDb.get_dict(self)
        if not l2 == None:
            value = cxt[info][l1][l2]
        else:
            value = cxt[info][l1]
        JsonDb.close(self)
        return value


if __name__ == '__main__':
    test = JsonDbJetty()
    print test.get_info('userinfo', 'chenyifan2016')
    print test.get_info('storageinfo', 'dir')
















































