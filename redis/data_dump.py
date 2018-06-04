#!/usr/bin/env python
# coding:utf-8
__author__ = 'stone'
__date__ = '2017/11/10'

import redis
from multiprocessing import Pool


src_ip = ''
src_port = 8000

target_ip = ''
target_port = 6379
target_passwd = '123456'

# 长连接
RedisSrcPool = redis.ConnectionPool(host=src_ip, port=src_port, db=10)
RedisSrcPool1 = redis.ConnectionPool(host=src_ip, port=src_port, db=11)
RedisSrcPool2 = redis.ConnectionPool(host=src_ip, port=src_port, db=12)
RedisSrcPool3 = redis.ConnectionPool(host=src_ip, port=src_port, db=13)
RedisSrcPool4 = redis.ConnectionPool(host=src_ip, port=src_port, db=14)

RedisTagetPool = redis.ConnectionPool(host=target_ip, port=target_port, password=target_passwd, db=0)
RedisTagetPool1 = redis.ConnectionPool(host=target_ip, port=target_port, password=target_passwd, db=1)
RedisTagetPool2 = redis.ConnectionPool(host=target_ip, port=target_port, password=target_passwd, db=2)
RedisTagetPool3 = redis.ConnectionPool(host=target_ip, port=target_port, password=target_passwd, db=3)
RedisTagetPool4 = redis.ConnectionPool(host=target_ip, port=target_port, password=target_passwd, db=4)


ser = redis.Redis(connection_pool=RedisTagetPool)
ser1 = redis.Redis(connection_pool=RedisTagetPool1)
ser2 = redis.Redis(connection_pool=RedisTagetPool2)
ser3 = redis.Redis(connection_pool=RedisTagetPool3)
ser4 = redis.Redis(connection_pool=RedisTagetPool4)


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
			ser1.zadd(key, value, float(score))  # 长连接
		if m_ttl != -1 and m_ttl is not None:
			ser1.expire(key, m_ttl)

	elif m_type == 'set':
		values = cl.smembers(key)
		for value in values:
			ser2.sadd(key, value)

		if m_ttl != -1 and m_ttl is not None:
			ser2.expire(key, m_ttl)

	elif m_type == 'hash':
		values = cl.hgetall(key)
		for hkey, hvalue in values.iteritems():
			ser3.hset(key, hkey, hvalue)
		if m_ttl != -1 and m_ttl is not None:
			ser3.expire(key, m_ttl)

	elif m_type == 'list':
		values = cl.lrange(key, 0, -1)
		for value in values:
			ser4.rpush(key, value)
		if m_ttl != -1 and m_ttl is not None:
			ser4.expire(key, m_ttl)


def start(cl):
	all_key = cl.keys('*')
	pool = Pool(processes=10)
	for key in all_key:
		pool.apply_async(get_client_key, args=(key,))

	pool.close()
	pool.join()


for i in range(0, 5):
	if i == 0:
		cl = redis.Redis(connection_pool=RedisSrcPool)
	elif i == 1:
		cl = redis.Redis(connection_pool=RedisSrcPool1)
	elif i == 2:
		cl = redis.Redis(connection_pool=RedisSrcPool2)
	elif i == 3:
		cl = redis.Redis(connection_pool=RedisSrcPool3)
	elif i == 4:
		cl = redis.Redis(connection_pool=RedisSrcPool4)
	start(cl)
