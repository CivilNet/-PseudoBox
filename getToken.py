# -*- coding: utf-8 -*-
import requests
import json

d_key="953f8d8013c549eeb6e2170c59639198"
d_name="jJshYk2_w"
d_secr="PQyMWdXsM0"
host = "https://aiot.gemfield.org:27032"

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
if __name__ == "__main__":
    getToken(d_key,d_name,d_secr)
