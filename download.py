#-*- coding:utf-8 -*-
import json
import hashlib
import requests
import sys
import os
from getToken import *
def download(data):
    data = json.loads(data)
    params = data["params"]
    files = params["file_list"]
    taskId = params["taskId"]
    for f in files:
        print(f)
        print("downloading with requests")
        url = f["url"] 
        r = requests.get(url,verify=False)
        local_path = str(f["local_path"])
        if not os.path.exists(local_path):
            os.mkdir(local_path)
        fn = url.split("/")[-1]
        fn = fn.split("%2F")[-1]
        with open(local_path+"/"+fn, "wb") as code:
            code.write(r.content)
        print(r.status_code)
        if r.status_code == 404:
            postDownFileStatus(taskId,"error")
        elif r.status_code == 200:
            postDownFileStatus(taskId,100)
def postDownFileStatus(taskId,status):
    url = '{}/south/report/issuedTask/progress'.format(host)
    response=requests.post(
        url,
        headers={'Content-Type': "application/json",'cache-control': 'no-cache','Connection': 'close'},
        data=json.dumps({"status":status,"token":getToken(d_key,d_name,d_secr),"taskId":taskId}),
        verify=False
    )
    print(response)
    print(response.url)
    print(response.status_code)
    print(response.content)

if __name__ == "__main__":
    download(sys.argv[1])
