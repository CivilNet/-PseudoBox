#!/usr/bin/env python
#coding=utf-8
import sys
import re
import os
import json
import numpy as np
import subprocess
import datetime
import cv2
from pydeepvac import SyszuxFace
import time
from zhiheutils import *
face = SyszuxFace('cuda')
#face = SyszuxFace('cpu')
face.loadDB('<人脸底库>')

REMOVE_DUPL_DICT = dict()
TIME=time.time()
def doface(path,sample,duration,threshold,upload_dir,taskid):
    global TIME
    vca = cv2.VideoCapture(path)
    frame_count = 0
    restart = 0
    status, frame = vca.read()
    while status:
        print("shape",frame.shape)
        if(time.time()-TIME>10):
            status = 1
            progress(status,taskid)
            TIME=time.time()
        if frame.shape[0] == 0:
            restart += 1
            if restart > 10000:
                vca.close()
                vca = cv2.VideoCapture(path)
                restart = 0
            status, frame = vca.read()
            continue
        frame_count += 1
        if frame_count % sample != 0:
            status, frame = vca.read()
            continue
        start = time.time()
        # detect face
        p_name = face.process(frame)
        if not p_name:
            status, frame = vca.read()
            continue
        for ind, one in enumerate(p_name):
            tmp = list(one)
            rate = (2-one[-1]**2)/2*0.43+0.57
            tmp[-1] = round(rate, 3)
            p_name[ind] = tuple(tmp)
        print(p_name)
        # recognition face
        personList = list()
        resultList = list()
        for i in range(len(p_name)):
            if p_name[i][-1] < threshold:
                person = "Unrecognized"
            else:
                person = p_name[i][1]
                resultList.append(p_name[i])
            personList.append(person)
        dupl_count = 0
        for person in personList:
            if (person == "Unrecognized"):
                continue
        if ((REMOVE_DUPL_DICT.get(person) is not None) and  time.time()-REMOVE_DUPL_DICT[person] < 4.5):
            dupl_count += 1
        if dupl_count == len(personList):
            print("dupl",time.time()-start)
            status, frame = vca.read()
            continue
        for person in personList:
            REMOVE_DUPL_DICT[person] = time.time()
        jsonList = []
        for result in resultList:
            person = dict()
            name = result[1]
            person["事件"]="人脸识别"
            person["名称"]=name
            person["时间"]=time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time()))
            jsonList.append(person)
        writePath = os.path.join(upload_dir,path.split('/')[-1]+"_"+str(time.time()) + ".jpg")
        cv2.imwrite(writePath, frame)
        dispose_data(writePath,jsonList,taskid)
        status, frame = vca.read()
if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv)!=2:
        exit("请输入python main.py str")
    data = eval(sys.argv[1])["params"]
    print(data)
    tenant_id=data["tenantId"]
    attributes = data['template']['属性']
    code = attributes['可订阅事件'][0]['事件码']
    if(code!='1'):
        exit("不是人脸检测任务")
    parameters = data['template']['参数']
    sample = int(parameters['采样率'])
    threshold = float(parameters['置信度'])
    taskid = data['taskId']
    path = 'rtsp://<name>:<password>@<ip>/cam/realmonitor?channel=1&subtype=1'
    progress(0,taskid)
    upload_dir = "./output/img/"
    if(not os.path.exists(upload_dir)):
        os.makedirs(upload_dir)
    duration = 15
    doface(path,sample,duration,threshold,upload_dir,taskid)
    print("done")
