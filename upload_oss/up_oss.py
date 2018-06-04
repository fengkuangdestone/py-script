#!/usr/bin/env python
# coding:utf-8
__author__ = 'stone'
__date__ = '2018/3/20'

import os
import oss2
import sys


filename = sys.argv[1]
upload_oss_dir = "upload/{0}".format(filename.split('/')[-1])
access_key_id = os.getenv('ACCESS_KEY_ID', '')
access_key_secret = os.getenv('ACCESS_KEY_SECRET', '')
endpoint = os.getenv('OSS_ENDPOINT', 'oss-cn-beijing.aliyuncs.com')
bucket_name = os.getenv('OSS_BUCKET_NAME', 'source-82722')
oss_connet_time = 5


bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret),
                     endpoint, bucket_name, connect_timeout=oss_connet_time)

result = bucket.put_object_from_file(upload_oss_dir, filename=filename)
print result.status
