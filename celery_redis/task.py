#!/usr/bin/env python
# coding:utf-8
__author__ = 'Stone'
__date__ = '2018/1/3'

from celery import Celery

brokers = 'redis://10.0.20.110:6379/5'
backend = 'redis://10.0.20.110:6379/6'

app = Celery("tasks", backend=backend, broker=brokers)


@app.task
def test(x, y):
    return x + y


# celery -A task worker --loglevel=info

# result = test.delay(3, 5)
# print result
# print result.ready()
# print result.get()
