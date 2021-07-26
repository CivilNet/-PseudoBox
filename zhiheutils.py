#! -*- coding:utf-8 -*-
import requests
import json
import time
import base64
from ctypes import *
host = "https://aiot.gemfield.org:27032"
url = host+'/south/report/analysisTask/result'
progress_url=host+'/south/report/analysisTask/progress'


d_key="953f8d8013c549eeb6e2170c59639198"
d_name="jJshYk2_w"
d_secr="PQyMWdXsM0"

def getToken(d_key,d_name,d_secr):
    data = {"deviceKey":d_key,"deviceName":d_name,"deviceSecret":d_secr}
    url = host+'/south/token'
    headers = {'content-type': "application/json"}
    r = requests.post(url, data=json.dumps(data), headers=headers,verify=False)
    if r.status_code == 200:
        print(r.text)
        data = json.loads(r.text)
        if data["code"] == "1":
            token = data["data"]["token"]
            print("getToken: {}".format(token))
            return token
token = getToken(d_key, d_name, d_secr)
def postData(taskid, imageFile, jsonList):

    fileData = open(imageFile, 'rb')
    fileData_b64 = base64.b64encode(fileData.read())
    fileData.close()
    for i in range(len(jsonList)):
       jsonList[i]["图片"]=fileData_b64.decode()
    data = dict()
    data["taskId"] = taskid
    data["channel"] = "1"
    data["token"] = token
    data["time"] = time.time()
    data["result"] = jsonList
    content = json.dumps(data)
    headers = {'content-type': "application/json"}
    r = requests.post(url, data=content, headers=headers, verify=False)
    print(r.text)
    if r.status_code == 200:
        data = json.loads(r.text)
        print(data)
    else:
        logging.info("Reported, server response: {}".format(r.text))
def progress(status,taskid):
    data = dict()
    data['status']=status
    data['taskId']=taskid
    data['token']=token
    content = json.dumps(data)
    print("content",content)
    headers = {'content-type': "application/json"}
    r = requests.post(progress_url, data=content, headers=headers, verify=False)
    print(r.text)
    if r.status_code == 200:
        data = json.loads(r.text)
        print(data)
        if data["code"] == "-1":
            print("失败")
    else:
        logging.info("Reported, server response: {}".format(r.text))

def dispose_data(imageFile,jsonList, taskid):
    postData(taskid, imageFile, jsonList)

import requests
import json
import base64
import socket
 
# 首先将图片读入
# 由于要发送json，所以需要对byte进行str解码
def getByte(path):
    with open(path, 'rb') as f:
        img_byte = base64.b64encode(f.read())
        img_str = img_byte.decode('ascii')
    return img_str

# img_str = getByte('/bigdata/niushaoda/srcface/1.jpg') 

# url = 'http://' + str(getIp()) + ':9888/'
# data = {'recognize_img':img_str, 'type':'0', 'useAntiSpoofing':'0'}
# json_mod = json.dumps(data)
# res = requests.post(url=url, data=json_mod)
# print(res.text)

