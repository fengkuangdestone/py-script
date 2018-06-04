#!/usr/bin/env python
# coding:utf-8
__author__ = 'stone'
__date__ = '2017/8/31'

import requests

url = ''
user = ''
password = ''


class SaltAPI(object):
	__token_id = ''
	
	def __init__(self):
		self.__url = url
		self.__user = user
		self.__password = password
	
	def token_id(self):
		""" user login and get token id """
		params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
		content = self.postRequest(params, prefix='/login')
		try:
			self.__token_id = content['return'][0]['token']
		except KeyError:
			raise KeyError
	
	def postRequest(self, obj, prefix='/'):  # post提交
		url = self.__url + prefix
		headers = {'X-Auth-Token': self.__token_id}
		resp = requests.post(
			url,
			data=obj,
			headers=headers,
			verify=False
		)
		return resp.json()
	
	def list_all_key(self):
		params = {'client': 'wheel', 'fun': 'key.list_all'}
		self.token_id()
		content = self.postRequest(params)
		minions = content['return'][0]['data']['return']['minions']
		minions_pre = content['return'][0]['data']['return']['minions_pre']
		return minions, minions_pre
	
	def delete_key(self, node_name):
		params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
		self.token_id()
		content = self.postRequest(params)
		ret = content['return'][0]['data']['success']
		return ret
	
	def accept_key(self, node_name):
		params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
		self.token_id()
		content = self.postRequest(params)
		ret = content['return'][0]['data']['success']
		return ret
	
	def remote_noarg_execution(self, tgt, fun):
		""" 无参数的命令 """
		params = {'client': 'local', 'tgt': tgt, 'fun': fun}
		self.token_id()
		content = self.postRequest(params)
		try:
			ret = content['return'][0][tgt]
		except Exception as a:
			ret = ""
		return ret
	
	def remote_execution(self, tgt, fun, arg):
		""" 有参数的命令 """
		params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
		self.token_id()
		content = self.postRequest(params)
		try:
			ret = content['return'][0][tgt]
		except Exception, e:
			ret = u'命令错误'
		return ret
	
	def target_remote_execution(self, tgt, fun, arg):
		""" Use targeting for remote execution """
		params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'nodegroup'}
		self.token_id()
		content = self.postRequest(params)
		try:
			jid = content['return'][0]['jid']
		except Exception, e:
			jid = "error"
		return jid
	
	def deploy(self, tgt, arg):
		""" Module deployment """
		params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
		self.token_id()
		content = self.postRequest(params)
		return content
	
	def async_deploy(self, tgt, arg):
		""" Asynchronously send a command to connected minions """
		params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
		self.token_id()
		content = self.postRequest(params)
		jid = content['return'][0]['jid']
		return jid
	
	def target_deploy(self, tgt, arg):
		""" Based on the node group forms deployment """
		params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
		self.token_id()
		content = self.postRequest(params)
		jid = content['return'][0]['jid']
		return jid


if __name__ == '__main__':
	sapi = SaltAPI()
	ret = sapi.remote_execution('*', 'cmd.run', 'ifconfig')
	print ret
