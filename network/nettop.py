#!/usr/bin/env python
# coding:utf-8
__author__ = 'stone'
__date__ = '2017/12/11'

import psutil
import time


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9.8 K'
    >>> bytes2human(100001221)
    '95.4 M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)


while True:
    pnic_before = psutil.net_io_counters(pernic=True)
    time.sleep(1)
    pnic_after = psutil.net_io_counters(pernic=True)
    nic_names = list(pnic_after.keys())
    nic_names.sort(key=lambda x: sum(pnic_after[x]), reverse=True)
    for name in nic_names:
        stats_before = pnic_before[name]
        stats_after = pnic_after[name]
        print (
	        name,
            "bytes-sent",
            bytes2human(stats_after.bytes_sent - stats_before.bytes_sent) + '/s',
            "bytes-recv",
            bytes2human(stats_after.bytes_recv - stats_before.bytes_recv) + '/s',
        )
