#!/usr/bin/env python
# coding:utf-8
__author__ = 'stone'
__date__ = '2017/8/29'

import smtplib, sys
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders

mail_host = 'smtp.exmail.qq.com'
mail_user = 'mail@mail.com'
mail_pass = ''


def main():
    """object=邮件测试  filename="file1,file2" text=内容 mail=mail@mail1.com,mail@mail2.com"""
    arg_data = []
    for arg in sys.argv[1:]:
        arg_data.append(tuple(arg.split('=')))
    data = dict(arg_data)

    if data.has_key('text') and data.has_key('object') and data.has_key('mail'):
        files = None
        text = data['text']
        subject = data['object']
        if data.has_key('filename'):
            files = data['filename'].split(',')
        receivers = data['mail'].split(',')
        status = SendEmail(subject, text, files, receivers)
        return status
    else:
        print sys.argv
        sys.exit(2)


def SendEmail(subject, text=None, files=None, receivers=None):
    message = MIMEMultipart()
    message.attach(MIMEText(text, 'plain', 'utf-8'))
    message['Subject'] = subject
    message['From'] = Header(mail_user)
    message['To'] = ','.join(receivers)

    if files is not None:
        for filename in files:
            if filename != '':
                with open(filename, 'rb') as f:
                    mime = MIMEBase('text', 'txt', filename=filename)
                    mime.add_header('Content-Disposition', 'attachment', filename=filename.split('/')[-1])
                    mime.set_payload(f.read())
                    encoders.encode_base64(mime)
                    message.attach(mime)

    try:
        smtpObj = smtplib.SMTP_SSL(timeout=5)
        smtpObj.connect(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        smtpObj.quit()
        smtpObj.close()
        return "邮件发送成功"
    except smtplib.SMTPException as e:
        smtpObj.quit()
        smtpObj.close()
        return e


if __name__ == '__main__':
    print main()
