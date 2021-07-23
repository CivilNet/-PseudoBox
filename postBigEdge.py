# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import json
import requests
import random
import hashlib
from getToken import *
from requests_toolbelt import MultipartEncoder
def getPartMd5(fs):
    m = hashlib.md5()
    m.update(fs)
    return m.hexdigest()
def getmd5(filepath):
    m = hashlib.md5()
    with open(filepath,'rb') as f:
        for line in f:
            m.update(line)
    return m.hexdigest()

def createUp(filepath,channel,token):
    info = dict()
    info["channel"] = channel
    info["fileSize"] = os.path.getsize(filepath)
    info["token"] = token
    info["type"] = 0
    #info["type"] = 1
    info["fileMd5"] = getmd5(filepath)
    return info

def postEdgeBig(data):
    url = '{}/south/edgeFile/upload/slice'.format(host)
    response=requests.post(
        url,
    	headers={'Content-Type': "application/json",'cache-control': 'no-cache','Connection': 'close'},
    	data=json.dumps(data),
        verify=False
    )
    print('------------------------------------------------------')
    print(response)
    print(response.url)
    print(response.status_code)
    print(response.content)
    return response.content
def postPartFile(f,sliceNo,uploadKey,token):
    j = 10
    id = []
    id = ''.join(str(i) for i in random.sample(range(0,11),j)) # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
    print(id)
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    uploadurl = '{}/south/file/upload/slice/put'.format(host)
    print(type(f))
    m= MultipartEncoder(
        fields={
            'sliceNo' : sliceNo,
            'uploadKey' : uploadKey,
            'fileMd5' : getPartMd5(f),
            'token': token,
            'file': ("uploadcloudtmp",f,'application/octet-stream')
        }
    )
    print(type(m))
    response=requests.post(
        uploadurl,
        headers={'Content-Type': m.content_type},
        data=m,
        timeout=None,
        verify=False
        )
    print(m.content_type)
    print('------------------------------------------------------')
    print(response)
    print(response.url)
    print(response.status_code)
    print(response.content)
    if response.status_code==200 and json.loads(response.content)["code"] == "1":
        print('upload filepart success')
    else:
        print('upload filepart failed')
def postEdgeMerge(uploadKey):
    print(uploadKey)
    token = getToken(d_key,d_name,d_secr)
    url = '{}/south/file/upload/slice/merge'.format(host)
    response=requests.post(
        url,
    	headers={'Content-Type': "application/json",'cache-control': 'no-cache','Connection': 'close'},
    	data=json.dumps({"uploadKey":uploadKey,"token":token}),
        verify=False
    )
    print(response)
    print(response.url)
    print(response.status_code)
    print(response.content)

if __name__ == "__main__":
    token = getToken(d_key,d_name,d_secr)
    local_path = "./test.mp4"
    params = json.loads(sys.argv[1])["params"]
    print(params)
    data = createUp(local_path,params["channel"],token)
    td = postEdgeBig(data)
    print(td)
    td = json.loads(td)
    f = open(local_path,"rb")
    nums = td["data"]["sliceCount"]
    partSize = td["data"]["size"]
    uploadKey = td["data"]["uploadKey"]
    for i in range(nums):
        postPartFile(f.read(partSize),str(i),uploadKey,token)
    f.close()
    postEdgeMerge(uploadKey)
