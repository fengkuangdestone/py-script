# _*_ coding:utf-8 _*_

import smtplib
from email.header import Header
from smail.utils import mail_encode, set_type

from smail.configs import smtp_cfg


class SendMail:
    def __init__(self, username, password, smtp_name='qqexmail', timeout=5):
        self.username = username
        self.password = password
        self.smtp_name = smtp_name
        self.timeout = timeout

    def send_mail(self, recipients, message):
        message = mail_encode(message)
        message['From'] = Header(self.username)
        recipients = set_type(recipients)

        cfg = smtp_cfg[self.smtp_name]
        host = cfg.get('host', None)
        port = cfg.get('port', None)

        try:
            server = smtplib.SMTP_SSL(host, port, timeout=self.timeout)
            server.login(self.username, self.password)

            message['To'] = ','.join(recipients)
            server.sendmail(self.username, recipients, message.as_string())
            # for recipient in recipients:
            #     message['To'] = recipient
            #     server.sendmail(self.username, recipient, message.as_string())
        except smtplib.SMTPException as e:
            print(e)
        finally:
            server.quit()
            server.close()


mail = {
    'subject': '[测试]test',
    'content': 'Dear All: \n\t测试测试',
    'attachments': '/test.py'
}
smtp_user = 'test@test.com'
smtp_pass = 'xxxx'
recipients = ['test@test.com', 'test1@test.com']

server = SendMail(username=smtp_user, password=smtp_pass)
print server.send_mail(recipients, mail)
