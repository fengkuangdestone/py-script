#!/usr/bin/env python
# coding:utf-8
__author__ = 'stone'
__date__ = '2017/8/24'
"""web质量检测"""
import pycurl, sys, os

URL = 'https://www.baidu.com'
USE_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
files = open(os.path.dirname(os.path.realpath(__file__)) + "/content.txt", "wb")

curl = pycurl.Curl()
curl.setopt(pycurl.URL, URL)
curl.setopt(pycurl.CONNECTTIMEOUT, 5)  # 连接等待时间
curl.setopt(pycurl.TIMEOUT, 5)  # 连接超时时间
curl.setopt(pycurl.FORBID_REUSE, 1)  # 交互后强制断开，不重用
curl.setopt(pycurl.DNS_CACHE_TIMEOUT, 60)  # 设置dns缓冲时间
curl.setopt(pycurl.MAXREDIRS, 5)  # 最大重定向次数
curl.setopt(pycurl.USERAGENT, USE_AGENT)  # 设置use_agent
curl.setopt(pycurl.WRITEHEADER, files)  # 将HEADER信息保存到文件对象中
curl.setopt(pycurl.WRITEDATA, files)  # 将HTML信息保存到文件对象中

try:
	curl.perform()
except Exception, e:
	curl.close()
	files.close()
	print "content errors: " + str(e)
	sys.exit()

HTTP_CODE = curl.getinfo(pycurl.HTTP_CODE)  # 状态码
NAMELOOKUP_TIME = curl.getinfo(pycurl.NAMELOOKUP_TIME)  # DNS解析时间
CONNET_TIME = curl.getinfo(pycurl.CONNECT_TIME)  # 建立连接时间
TOTAL_TIME = curl.getinfo(pycurl.TOTAL_TIME)  # 传输时间
SIZE_DOWNLOAD = curl.getinfo(pycurl.SIZE_DOWNLOAD)  # 下载包大小
SPEEND_DOWNLOAD = curl.getinfo(pycurl.SPEED_DOWNLOAD)  # 平均下载速度

curl.close()
files.close()

# print HTTP_CODE
print "HTTP状态码: %s" %HTTP_CODE
print "DNS解析时间: %.2f ms" %NAMELOOKUP_TIME
print "建立连接时间: %.2f ms" %CONNET_TIME
print "传输时间: %.2f ms" %TOTAL_TIME
print "下载包大小: %d byte" %SIZE_DOWNLOAD
print "平均下载速度: %d bytes/s" %SPEEND_DOWNLOAD

