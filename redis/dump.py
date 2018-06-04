#!/usr/bin/env python
# coding:utf-8
__author__ = 'stone'
__date__ = '2017/11/10'

import redis
from multiprocessing import Pool
import sys
import time

src_ip = '127.0.0.1'
src_port = 6379

target_ip = '127.0.0.1'
target_port = 8000
target_passwd = 'xxxx'

keys = sys.argv[1]
src_db = sys.argv[2]
target_db = sys.argv[3]

# 长连接
RedisSrcPool = redis.ConnectionPool(host=src_ip, port=src_port, db=src_db)
RedisTagetPool = redis.ConnectionPool(host=target_ip, port=target_port, password=target_passwd, db=target_db)
ser = redis.Redis(connection_pool=RedisTagetPool)
cl = redis.Redis(connection_pool=RedisSrcPool)


# 普通tcp
# cl = redis.StrictRedis(host=src_ip, port=8000, db=10)
# ser = redis.StrictRedis(host=target_ip, port=6379, db=0, password='123456')

def get_client_key(key):
	m_type = cl.type(key)
	m_ttl = cl.ttl(key)

	if m_type == 'string':
		val = cl.get(key)
		if m_ttl == -1 and m_ttl is not None:
			ser.set(key, value=val)
		else:
			ser.set(key, value=val, ex=m_ttl)

	elif m_type == 'zset':
		values = cl.zrange(key, 0, -1)
		for value in values:
			score = cl.zscore(key, value)
			# ser.zadd(key, float(score), value)  # 普通tcp add
			ser.zadd(key, value, float(score))  # 长连接
		if m_ttl != -1 and m_ttl is not None:
			ser.expire(key, m_ttl)

	elif m_type == 'set':
		values = cl.smembers(key)
		for value in values:
			ser.sadd(key, value)

		if m_ttl != -1 and m_ttl is not None:
			ser.expire(key, m_ttl)

	elif m_type == 'hash':
		values = cl.hgetall(key)
		for hkey, hvalue in values.iteritems():
			ser.hset(key, hkey, hvalue)
		if m_ttl != -1 and m_ttl is not None:
			ser.expire(key, m_ttl)

	elif m_type == 'list':
		values = cl.lrange(key, 0, -1)
		for value in values:
			ser.rpush(key, value)
		if m_ttl != -1 and m_ttl is not None:
			ser.expire(key, m_ttl)


def start():
	if keys == '*':
		all_key = cl.keys('*')
	else:
		all_key = cl.keys(keys+'*')
	pool = Pool(processes=10)
	for key in all_key:
		pool.apply_async(get_client_key, args=(key,))

	pool.close()
	pool.join()


if __name__ == '__main__':
	print "start time: " + time.strftime("%Y-%m-%d %H:%M:%S")
	print start()
	print "stop time:" + time.strftime("%Y-%m-%d %H:%M:%S")
