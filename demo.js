var IotDevice = require("./sdk/iot_device")
var request=require('request')
var moment = require('moment');
require('dotenv').config()
var path = require('path')
const fs = require('fs');
const { spawn } = require('child_process');
var device = new IotDevice({
    productName: process.env.PRODUCT_NAME,
    deviceName: process.env.DEVICE_NAME,
    secret: process.env.SECRET,
    clientID: path.basename(__filename, ".js"),
    storePath: `./tmp/${path.basename(__filename, ".js")}`

})
device.on("online", function () {
    console.log("device is online")
})
let python = null
let upload = null
let livepid = null
let dfload = null
device.on("command", async function (command, requestId, data, respondCommand) {
    console.log(1,command)
    console.log(2,requestId)
    data = JSON.parse(data)
    console.log(3,data)
    if (command == "livestream") {
        let channel = data.params.channel
        let control = data.params.action
        let url = data.params.url
        console.log(data)
        if (control == "start"){
            if (livepid){
                console.log("livepid is running")
                return
            }
            livepid = spawn("ffmpeg",["-i","rtsp://<username>:<password>@<ip>/cam/realmonitor?channel=1&subtype=1","-vcodec","libx264","-acodec","aac","-ar",48000,"-r",25,"-f","flv",`${url}`], {shell: false})
            // livepid = spawn("ffmpeg",["-re","-stream_loop",-1,"-i","./test.mp4","-vcodec","libx264","-acodec","aac","-ar",48000,"-r",25,"-f","flv","-strict","-2",`${url}`], {shell: false})
            livepid.stdout.on('data',(data) => {
                console.log(data.toString())
            });
            livepid.stderr.on('data', (data) => {
                console.error(`livepid stderr: ${data}`);
            });
            livepid.on('close', (code) => {
                if (code !== 0) {
                    console.log(`livepid 进程退出，退出码 ${code}`);
                }
                livepid = null
            });
        } else {
	    if (livepid){
	        livepid.kill()
		livepid = null
	    }
            console.log("livepid stoped")
        }
    }else if(command == "getroot" || command == "ls") {
        let path = "/"
        if (command == "ls"){
            path = data.params.path
        }
        console.log(path)
        let ls = spawn('python3', ['getDir.py',`${path}`,`${requestId}`],{shell: false})
        console.log(111111)
        ls.stdout.on('data',(data) => {
            console.log(data.toString())
        });
        ls.stderr.on('data', (data) => {
            console.error(`ls stderr: ${data}`);
        });
        ls.on('close', (code) => {
            if (code !== 0) {
                console.log(`ls 进程退出，退出码 ${code}`);
            }
        });
    }else if(command == "record") {
        let str = JSON.stringify(data,null,"\t")
        console.log(str)
        let up = spawn('python3', ['postBigEdge.py',`${str}`],{shell: false})
        up.stdout.on('data',(data) => {
            console.log(data.toString())
        });
        up.stderr.on('data', (data) => {
            console.error(`up stderr: ${data}`);
        });
        up.on('close', (code) => {
            if (code !== 0) {
                console.log(`up 进程退出，退出码 ${code}`);
            }
        });
    } else if (command == "config"){
        let str = JSON.stringify(data.params,null,"\t")
        console.log(str)
        let res = data.params.channels
        let aiTable = data.params.aiTable
        let feaTable = data.params.feaTable
        console.log(res)
        console.log(aiTable)
        console.log(feaTable)
        res.forEach(function(v,index,a){
            v["ai"].forEach(function(va,i,aa){
            res[index].ai[i]={"AI能力名称":aiTable[va.index]["AI能力名称"],"算法版本":aiTable[va.index]["算法版本"],"底库名称":feaTable[va.feaIndex]["底库名称"],"底库版本":feaTable[va.feaIndex]["底库版本"]}
            });
        });
        console.log(res)
        fs.writeFile('aiconfig.conf', JSON.stringify(res), function (err) {
            console.log(err)
            if (err) throw err;
            console.log('It\'s saved!');
        });
    } else if (command == "download"){
        let str = JSON.stringify(data,null,"\t")
        console.log(str)
        dfload = spawn('python3', ['download.py',`${str}`],{shell: false})
        dfload.stdout.on('data',(data) => {
            console.log(data.toString())
        });
        dfload.stderr.on('data', (data) => {
            console.error(`python stderr: ${data}`);
        });
        dfload.on('close', (code) => {
            if (code !== 0) {
                console.log(`dfload 进程退出，退出码 ${code}`);
            }
            dfload = null
        });
    } else if (command == "upload"){
        if (upload){
            console.log("file upload is running")
            return
        }
        let str = JSON.stringify(data,null,"\t")
        console.log(str)
        upload = spawn('python3', ['postBigCloud.py',`${str}`],{shell: false})
        upload.stdout.on('data',(data) => {
            console.log(data.toString())
        });
        upload.stderr.on('data', (data) => {
            console.error(`upload stderr: ${data}`);
        });
        upload.on('close', (code) => {
            if (code !== 0) {
                console.log(`upload 进程退出，退出码 ${code}`);
            }
            upload = null
        });
    } else if (command == "inference"){
        let control = data.params.action
        let str = JSON.stringify(data,null,"\t")
        console.log(str)
        if (control == "start"){
            if (python){
                console.log("face detect is running")
                return
            }
            python = spawn('python3', ['main.py', `${str}`],{shell: false})
            // python = spawn('python3', ['postBigTask.py', `${str}`],{shell: false})
            python.stdout.on('data',(data) => {
                console.log(data.toString())
            });
            python.stderr.on('data', (data) => {
                console.error(`python stderr: ${data}`);
            });
            python.on('close', (code) => {
                if (code !== 0) {
                    console.log(`face detect 进程退出，退出码 ${code}`);
                }
                python = null
            });
        } else {
	    if (python){
	        python.kill()
                console.log("face detect task stoped")
		python = null
	    }
            console.log("task stoped")
        }
    }
})
device.connect()

var CronJob = require('cron').CronJob;
new CronJob('*/30 * * * * *', function() {
    fs.readFile('aiconfig.conf', function (error, data) {
        if (error) {
            console.log('读取文件失败了')
        } else {
        moment.locale('zh-cn');
        let _today = moment();
        let res = {"devname":"S100测试机","channels":[]}
        res["update_time"] = _today.format('YYYY-MM-DD HH:mm:ss');
        data = data.toString()
        array = JSON.parse(data)
        array.forEach(function(v,index,a){
            v["status"] = "online"
            res["channels"].push(v)
        });
        st = {"update_time":res["update_time"],"ip":"192.194","mac":"84:B0","serial_number":"037430","name":"s1","type":"智盒","location":"15F","model":"s1","soft_ware_ver":"v0.3","baseline_ver":"R321","channels":[{"vendor":"UNIVIEW","rtsp":"rtsp://media/video1","ip":"19","channel":0,"ipcid":"IPC-ID$UNIVI$","location":"f15","longitude":"东经","latitude":"北纬"}],"ai_capability":["capture"]}
        //console.log(st)
        device.updateStatus(st)

        data = JSON.stringify(res)
        device.uploadData(data,"health")
        console.log(data)
        }
    })
    console.log("report health data for onetime")
},null,true)

