#!/usr/bin/env python
# coding:utf-8
__author__ = 'stone'
__date__ = '2018/1/2'

import logging
from logging import INFO, DEBUG, WARNING, ERROR

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer

bind_addr = '0.0.0.0'
port = 21

max_connects = 256
max_connects_pre_ip = 5

read_limit = 30 * 1024  # 30 kb/sec
write_limit = 30 * 1024  # 30 kb/sec

log_file = './ftp.log'
log_level = INFO

user_list = [
    {'name': 'carey', 'passwd': 'passwd', 'homedir': '/home/carey', 'perm': 'elradfmwMT'},
    {'name': 'test', 'passwd': 'test', 'homedir': '/home/test', 'perm': 'elradfmwMT'},
]


authorizer = DummyAuthorizer()
for user in user_list:
    authorizer.add_user(user['name'], user['passwd'], user['homedir'], perm=user['perm'])

dtp_handler = ThrottledDTPHandler
dtp_handler.read_limit = read_limit
dtp_handler.write_limit = write_limit

handler = FTPHandler
# handler.passive_ports = range(2000, 2300)  # 被动模式
handler.authorizer = authorizer
handler.dtp_handler = dtp_handler

logging.basicConfig(filename=log_file, level=log_level)

server = FTPServer((bind_addr, port), handler)
server.max_cons = max_connects
server.max_cons_per_ip = max_connects_pre_ip
server.serve_forever()
