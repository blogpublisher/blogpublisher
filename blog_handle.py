#!/usr/bin/python
# encoding: utf-8
import poplib
import sys
import re
import shutil

import ConfigParser
import string, os
import socket
#from email import parser

import email
from email.parser import Parser
from email.header import decode_header
from email.header import Header
from email.utils import parseaddr
from blog_handle import *
import fileinput
from jsondb.jsondb import *
from tools import tohex

class BlogHandle:
    pass

class BlogHandleEmail(BlogHandle):
    def __init__(self, pop3input=None, index=None):
        self.pop3input = pop3input
        self.index =index
        self.subject = None
        self.blogclass= None
        self.blogtitle= None
        self.blog_body= None

    def guess_charset(self, msg):
        charset = msg.get_charsets()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def print_info(self, msg, indent=0):
        if indent == 0:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header=='Subject':
                        value = self.decode_str(value)
                        self.subject = value
                    else:
                        hdr, addr = parseaddr(value)
                        name = self.decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)
                        #print('%s%s: %s' % (' ' * indent, header, value))

        if (msg.is_multipart()):
            print 'content type:' + msg.get_content_type()
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                print('%spart %s' % (' ' * indent, n))
                print('%s--------------------' % (' ' * indent))
                self.print_info(part, indent + 1)
        else:
            content_type = msg.get_content_type()
            charset = self.guess_charset(msg)
            filename = msg.get_filename()
            if filename:
                h = Header(filename)
                dh = decode_header(h)  #[('brain.jpg', None)]
                print dh
                print "have attachment and save attachment " + dh[0][0]
                fname = dh[0][0]
                encodeStr = dh[0][1]
                print '%s,%s' % (fname, encodeStr)
                if encodeStr != None:
                    if charset == None:
                        fname = fname.decode(encodeStr, 'gbk')
                        #else:
                        #  fname = fname.decode(encodeStr, charset)

                data = msg.get_payload(decode=True)
                db = JsonDbJetty()
                media_buf_dir = db.get_info('media', 'buff_dir')
                self.savefile(fname, data, media_buf_dir)

            elif content_type=='text/plain':
                content = msg.get_payload(decode=True)
                charset = self.guess_charset(msg)
                if charset:
                    content = content.decode(charset[0])

                db = JsonDbJetty()
                rawfile = db.get_info('article', 'raw_file')
                fp=open(rawfile,'wb')
                fp.truncate()
                fp.write(content)
                fp.close()
            elif content_type=='text/html':
                print 'content_type == text/html ignore it !!!'
            else:
                print('%sAttachment: %s' % (' ' * indent, content_type))

    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def savefile(self, filename, data, path):
        try:
            filepath = path + '/' + filename
            print 'Saved as ' + filepath
            f = open(filepath, 'wb')
        except:
            print('filename error')
            f.close()
        f.write(data)
        f.close()

    def get_email(self):
        resp, lines, octets = self.pop3input.retr(self.index)
        msg_content = '\r\n'.join(lines)
        msg = Parser().parsestr(msg_content)

        self.print_info(msg)
        self.parse_email()

    def get_blog_user(self):
        return self.subject

    def parse_email(self):
        db = JsonDbJetty()
        rawfile = db.get_info('article', 'raw_file')
        bodyfile = db.get_info('article', 'body_file')
        shutil.copyfile(rawfile, bodyfile)
        cxt_flag = False
        regx = re.compile('^,,,,$')
        for l in fileinput.input(bodyfile, inplace=True):
            if cxt_flag == True:
                #print l
                sys.stdout.write(l)
            else:
                theline = l.strip()
                if regx.match(theline):
                    cxt_flag = True
                    continue
                if theline.startswith('class='):
                    self.blogclass=theline.replace('class=','')
                    continue
                if theline.startswith('title='):
                    self.blogtitle=theline.replace('title=','')
                    continue
        fileinput.close()
        if self.blogclass and self.blogtitle and cxt_flag==True:
            return 1
        else:
            return 0

    def get_title(self):
        return self.blogtitle

    def get_class(self):
        return self.blogclass

    def save_email(self):
        pass
