#!/usr/bin/env python
# coding:utf-8
__author__ = 'stone'
__date__ = '2017/8/24'

import sys, os, paramiko
from config import Config


def main(argv):
	help = """help: \n\t%s group=[ group ] cmd=[ "cmd" ]""" %argv[0].split('/')[-1]
	arg_data = []
	if len(argv[1:]) == 2:
		for arg in argv[1:]:
			arg_data.append(tuple(arg.split('=')))
		data = dict(arg_data)

		if data.has_key('group') and data.has_key('cmd'):
			return data
		else:
			print help
			sys.exit(1)
	else:
		print help
		sys.exit(1)


def get_config(name):
	f = file('cnf.cfg')
	cfg = Config(f)
	try:
		data = cfg[name]
		return data
	except None:
		return False


def paramiko_cmd(ip):
	arg = main(sys.argv)
	cnf = get_config(arg['group'])
	paramiko.util.log_to_file(get_config('logfile'))
	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	try:
		if cnf['is_pkey']:
			privatekey = os.path.expanduser(get_config('private_key_file'))
			key = paramiko.RSAKey.from_private_key_file(privatekey)
			ssh.connect(
				hostname=ip,
				port=cnf['port'],
				username=cnf['username'],
				pkey=key,
				timeout=cnf['timeout'],
				compress=cnf['compress']
			)
		else:
			ssh.connect(
				hostname=ip,
				port=cnf['port'],
				username=cnf['username'],
				password=cnf['password'],
				timeout=cnf['timeout'],
				compress=cnf['compress']
			)
	except Exception, e:
		ssh.close()
		print e
		sys.exit(1)
	stdin, stdout, stderr = ssh.exec_command(arg['cmd'])
	data = stdout.read()
	ssh.close()
	return data


if __name__ == "__main__":
	for ip in get_config(main(sys.argv)['group'])['hostname']:
		print "%s %s commond: %s \n%s" %('#'*10, ip, '#'*10, paramiko_cmd(ip=ip))
