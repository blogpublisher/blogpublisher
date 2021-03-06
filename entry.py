#!/usr/bin/python
# encoding: utf-8
import sys
import string, os
from time import sleep
from inbox import *
from blog_handle import *
from send_mail import MyMail
reload(sys)
sys.setdefaultencoding('utf8')

def process_blog(svr, index):
    handle = BlogHandleEmail(svr, index)
    handle.get_email()

    blog_user = handle.get_blog_user()
    category = handle.get_class()
    title = handle.get_title()
    cur_blog = BlogJetty(category, title, blog_user)

    if cur_blog.authinfo() == None:
        cur_blog.clean_datas()
        m = MyMail()
        m.send('Blog publish Failed!!!','The subject: ['+blog_user+'] not exist!')
        return False
    cur_blog.parse_article_header()
    cur_blog.parse_article_body()
    cur_blog.save_article()
    cur_blog.save_media()
#    cur_blog.article_upload_server()
#    cur_blog.media_upload_server()
    cur_blog.clean_datas()
    cur_blog.send_email()
    return True


def main():
    inbox = Pop3Input()
    ret = inbox.login()
    if not ret == 0:
        print 'Error receive email!'
        return 1

    svr = inbox.get_server()
    idx = inbox.get_index()
    print idx
    old_idx = inbox.get_db_index()
    old_idx = int(old_idx)
    if old_idx ==idx :
        print 'no new email!!!'
        #process_blog(svr, 246)
        return 0

    if old_idx == 0:
        old_idx = idx
        if not process_blog(svr, idx):
            return 0
        inbox.set_db_index(idx)
        return 1

    if old_idx < idx:
        f = old_idx+1
        t = idx+1
        for cur in range(f, t):
            if not process_blog(svr, cur):
                return 0
            inbox.set_db_index(idx)
            sleep(5)

        return 1


if __name__ == '__main__':
    main()
