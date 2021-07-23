# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import requests
import random
from getToken import *
from requests_toolbelt import MultipartEncoder

def postEdgeFile(filepath,channel,ftype):
    j = 10
    id = []
    id = ''.join(str(i) for i in random.sample(range(0,11),j)) # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
    print id
 
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    uploadurl = '{}/south/edgeFile/upload'.format(host)
    f = open(filepath,'rb')
    print(type(f))
    m= MultipartEncoder(
        fields={
            'channel': str(channel),
            'type': str(ftype),
            'token': getToken(d_key,d_name,d_secr),
            'file': (f.name,f,'application/octet-stream')
        }
    )
    print(type(m))
    print(m)
    
    response=requests.post(
        uploadurl,
    	headers={'Content-Type': m.content_type},
    	data=m,
    	timeout=None,
        verify=False
    	)
    f.close()
    print m.content_type
    print m
    print '------------------------------------------------------'
    print response
    print response.url
    print response.status_code
    print response.content
    if response.status_code==200:
        print 'upload success'
    else:
        print 'upload failed'
if __name__ == "__main__":
    postEdgeFile(sys.argv[1],sys.argv[2],sys.argv[3])
