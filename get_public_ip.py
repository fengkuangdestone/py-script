#!/usr/bin/env python
# coding:utf-8

import requests, json


class GET_IP(object):
		def __init__(self, url,url1):
				self.url = url
				self.url1 = url1

		def Get_ip(self):
				data = requests.get(url).text
				return data
		def Get_public(self):
				URL = url1 + datas
				Data = requests.get(URL).text
				DAta = json.loads(Data)
				return DAta


if __name__ == '__main__':
		url = 'http://icanhazip.com/'
		url1 = 'http://ip.taobao.com/service/getIpInfo.php?ip='
		DATA = GET_IP(url,url1)
		datas = DATA.Get_ip()
		coure = DATA.Get_public()
		print coure['data']