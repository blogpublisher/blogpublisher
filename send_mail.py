#!/usr/bin/python
#-*-coding:utf-8-*-
import smtplib
import sys
from email.Header import Header
from email.mime.text import MIMEText

class MyMail:
    def __init__(self, mailServer, username, password):
        self.mailServer = mailServer
        self.username = username
        self.password = password
        self.conn = None

    def send_mail(self, f, t, msg):
        try:
            self.conn = smtplib.SMTP()
            self.conn.connect(self.mailServer)
            self.conn.login(self.username, self.password)
            self.conn.sendmail(f, t, msg.as_string())
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
        msg['Subject'] = 'Blog published:'+subject
        return self.send_mail(me,mailTo,msg)

    def send(self, subject, txt):
        self.send_text('xxx', ['xxx',  'xxx'], subject, txt)
