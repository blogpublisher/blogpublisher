#!/usr/bin/python
#-*-coding:utf-8-*-
import poplib
import sys
import fileinput
import re
import shutil

import ConfigParser
import string, os
import datetime
from jsondb.jsondb import *
from expectgit.expectgit import *
from send_mail import *

class Blog:
    def __init__(self,article_categories, article_title, blog_name):
        self.article_categories = article_categories
        self.article_title = article_title
        self.article_filename = None
        self.article_dir = None
        self.blog_name = blog_name
        self.db = JsonDbJetty()

    def parse_article_header(self):
        partern_title = re.compile(self.db.get_info('article', 'title'))
        partern_cate = re.compile(self.db.get_info('article', 'cate'))
        f1 = self.db.get_info('article', 'h_tmpl_file')
        f2 = self.db.get_info('article', 'h_file')
        shutil.copyfile(f1, f2)
        for line in fileinput.input(f2, inplace=True):
            if partern_title.search(line):
                print partern_title.sub(self.article_title, line).strip()
            elif partern_cate.search(line):
                print partern_cate.sub(self.article_categories, line).strip()
            else:
                print line.strip()
        fileinput.close()
        print 'create ok'

    def is_update_article(self):
        blog_dir = self.db.get_info('user', self.blog_name, 'dir')
        catedir = blog_dir + '/_posts/' + self.article_categories
        if not os.path.exists(catedir):
            return False
        bakdir = os.getcwd()
        os.chdir(catedir)
        print self.article_title
        for line in fileinput.input(os.listdir(catedir)):
            if line.startswith('title:'):
                #if line.find(self.article_title):
                if self.article_title in line:
                    print '==find the blog and get the file name=='
                    self.article_filename = fileinput.filename()
                    print self.article_filename
                    fileinput.close()
                    os.chdir(bakdir)
                    return True
                else:
                    print '==not find the blog and get the file name=='


        fileinput.close()
        os.chdir(bakdir)
        return False

    def create_article_filename(self):
        if self.is_update_article():
            return True
        now = datetime.datetime.now()
        self.article_filename = now.strftime(self.db.get_info('article', 'date'))
        self.article_filename = self.article_filename + self.article_categories
        self.article_filename = self.article_filename + '.md'
        print self.article_filename
        return False

    def create_article_dir(self):
        self.article_dir = self.db.get_info('user', self.blog_name, 'dir')
        self.article_dir = self.article_dir + '/_posts/' + self.article_categories
        if not os.path.exists(self.article_dir):
            os.makedirs(self.article_dir)
        return self.article_dir

    def create_media_dir(self):
        temp = self.db.get_info('storage', 'dir')
        temp = temp + '/'+self.db.get_info('user', self.blog_name, 'username')
        temp = temp + '/_posts/'
        temp = temp + self.article_categories
        temp = temp + '/' + self.article_filename
        self.blog_media_dir = temp
        if not os.path.exists(self.blog_media_dir):
            os.makedirs(self.blog_media_dir)

    def parse_article_body(self):
        self.create_article_filename()
        match = self.db.get_info('article', 'pic_url_match')
        p=re.compile(match)
        bodyfile = self.db.get_info('article', 'body_file')
        u = self.db.get_info('user', self.blog_name, 'username')
        for line in fileinput.input(bodyfile, inplace=True):
            match = p.match(line)
            if match:
                if match.group(5):
                    matchline = match.group(1)
                    matchline = matchline + match.group(2)
                    matchline = matchline + match.group(3)
                    matchline = matchline + match.group(4)
                    matchline = matchline + match.group(5)
                    matchline = matchline + self.db.get_info('storage', 'url')
                    matchline = matchline + '/' + u
                    matchline = matchline + '/_posts'
                    matchline = matchline + '/' + self.article_categories
                    matchline = matchline + '/' + self.article_filename
                    matchline = matchline + '/' + match.group(6)+'?raw=true'
                    matchline = matchline + match.group(7)
                    matchline = matchline + match.group(8)
                    print matchline
            else:
                sys.stdout.write(line)

        fileinput.close()

    def save_article(self):
        self.create_article_dir()
        fname = self.article_dir + '/' + self.article_filename

        f=open(fname, 'wb')
        f.truncate()
        header = self.db.get_info('article', 'h_file')
        body = self.db.get_info('article', 'body_file')
        filelist = [header, body]
        for line in fileinput.input(filelist):
            f.write(line)
        f.close()
        fileinput.close()

    def save_media(self):
        lis = []
        self.create_media_dir()
        buff_dir = self.db.get_info('media', 'buff_dir')
        fs = os.listdir(self.db.get_info('media', 'buff_dir'))
        for f in fs:
            shutil.copy(buff_dir + '/' +f, self.blog_media_dir)

    def article_upload_server(self):
        git_tool = Expectgit()
        dir = self.db.get_info('user', self.blog_name, 'dir')
        u = self.db.get_info('user', self.blog_name, 'username')
        p = self.db.get_info('user', self.blog_name, 'password')
        git_tool.git_expect(dir, u, p)

    def media_upload_server(self):
        git_tool = Expectgit()
        u = self.db.get_info('storage', 'username')
        p = self.db.get_info('storage', 'password')
        dir = self.db.get_info('storage', 'dir')
        git_tool.git_expect(dir, u, p)

class BlogJetty(Blog):
    def __init__(self,article_categories, blog_title, blog_name):
        Blog.__init__(self, article_categories, blog_title, blog_name)

    def clean_datas(self):
        buff_dir = self.db.get_info('media', 'buff_dir')
        bakdir = os.getcwd()
        os.chdir(buff_dir)
        fs = os.listdir(buff_dir)
        for f in fs:
            if os.path.exists(f):
                os.remove(f)
        os.chdir(bakdir)
        h_file = self.db.get_info('article', 'h_file')
        if os.path.exists(h_file):
            os.remove(h_file)

        body_file = self.db.get_info('article', 'body_file')
        if os.path.exists(body_file):
            os.remove(body_file)

        raw_file = self.db.get_info('article', 'raw_file')
        if os.path.exists(raw_file):
            os.remove(raw_file)
        return True

    def send_email(self):
        url = self.db.get_info('user', self.blog_name, 'http')
        txt = 'your blog has published!\r\n\r\n %s' % url
        s = MyMail('smtp.xxx', 'xxx', 'xxx')
        s.send(self.article_title, txt)


if __name__ == '__main__':
    blog = 'chenyifan2016'
    category = 'life'
    title = 'monday'

    obj = BlogJetty('life', 'monday', 'chenyifan2016')
    obj.parse_article_header()
    obj.parse_article_body()
    obj.save_article()

