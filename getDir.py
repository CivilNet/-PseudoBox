# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import json
import requests
import random
from getToken import *

def getDir(path):
    return os.listdir(path)

def getFileInfo(path):
    info = dict()
    statinfo = os.stat(path)
    _,info["name"] = os.path.split(path)
    info["time"] = statinfo.st_mtime*1000
    info["path"] = path
    if os.path.isfile(path):
        info["isDir"] = False
        info["size"] = statinfo.st_size
    else:
        info["isDir"] = True
    return info

def postDir(path,reqId):
    print(path,reqId)
    filelist = []
    for f in getDir(path):
        if path != "/":
            filelist.append(getFileInfo(path+"/"+f))
        else:
            filelist.append(getFileInfo("/"+f))
    print(filelist)
    token = getToken(d_key,d_name,d_secr)
    print(getToken(d_key,d_name,d_secr))
    data = json.dumps({"token":token,"reqId":reqId,"list":filelist})
    print(data)
    url = '{}/south/callback'.format(host)
    response=requests.post(
        url,
    	headers={'Content-Type': "application/json",'cache-control': 'no-cache','Connection': 'close'},
    	data=data,
        verify=False
    )
    print('------------------------------------------------------')
    print(response)
    print(response.url)
    print(response.status_code)
    print(response.content)
    if response.status_code==200:
        print('ls success')
    else:
        print('ls failed')
if __name__ == "__main__":
    postDir(sys.argv[1],sys.argv[2])
