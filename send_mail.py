#!/usr/bin/python
#-*-coding:utf-8-*-
import smtplib
import sys
from email.Header import Header
from email.mime.text import MIMEText
from jsondb.jsondb import *
from tools import *
class MyMail:
    def __init__(self):
        self.conn = None
        self.db = JsonDbJetty()

    def send_mail(self, f, t, msg):
        try:
            server = self.db.get_info('notify', 'server')
            password = self.db.get_info('notify', 'password')
            user= self.db.get_info('notify', 'user')
            self.conn = smtplib.SMTP()
            self.conn.connect(server)
            self.conn.login(user, password)
            self.conn.sendmail(f, t, msg.as_string())
            self.conn.close()
            return True
        except Exception,e:
            print 'error send_mail'
            return False


    def send_text(self,mailFrom,mailTo,subject,text):
        msg = MIMEText(str(text),'plain','utf-8')
        me = ('%s<'+mailFrom+'>') % (Header(mailFrom,'utf-8'),)
        msg['From'] = me
        msg['To'] = ','.join(mailTo)
        if not isinstance(subject, unicode):
            subject=unicode(subject, 'utf-8')
        msg['Subject'] = subject
        return self.send_mail(me,mailTo,msg)

    def send(self, subject, txt):

        receivers = self.db.get_info('notify', 'receivers')
        sender = self.db.get_info('notify', 'user')
        lists = receivers.split(',')
        self.send_text(sender, lists, subject, txt)

