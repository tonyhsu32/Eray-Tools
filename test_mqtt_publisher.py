import paho.mqtt.client as mqtt
from datetime import datetime
import json
import requests
from typing import Optional
# from pydantic import BaseModel

def read_file(path):
    with open(path, "rb") as f:
        base64_img = f.read()
        base64_img = base64_img.decode("utf-8")

    return base64_img

facedevice_back = {
    "code": 0,
    "msg": "Upload Person Info!",
    "device_id": "7101389947744",
    "dev_cur_pts": 1583996959,
    "tag": "UploadPersonInfo",
    "datas":
        {
            "msgType": "1",
            "similar": "98",
            "user_id": "77",
            "name": "xiaoming", 
            "time": str(datetime.now()), 
            "temperature": "36.60",
            "matched": "0", 
            "imageFile": "data:image/jpeg;base64," + read_file("/home/eray/Documents/AUO_CIC/ex_base64_no_DataURL.txt")
        }
}

# 每日人員異常提醒 api
site = "siteC"
api_host = f"https://asia-east1-panasiasmartsitesapp.cloudfunctions.net/api/siteA/ppe/event/add"

fake_person_data = {
	"exceptionList": [
		{
			"contractor": "eray_fake",
			"correctAmount": 1,
			"exceptionAmount": 1,
			"exceptions": [
				{
					"name": "eray_tony",
					"entryTime": str(datetime.now()),
					"exitTime": "",
					"exceptionLog": "只有進",
					"photoUrl": "data:image/jpeg;base64," + read_file("/home/eray/Documents/AUO_CIC/ex_base64_no_DataURL.txt")
				},
			]
		}
	]
}

fake_ppe_data = {
    "event_level": 1,
    "event_code": 9,
    "device_id": "axis-003",
    "detect": "有穿戴安全帽",
    "note": "",
    "img_data": ""
}

# 建立 MQTT Client 物件
client = mqtt.Client()

# 設定登入帳號密碼（若無則可省略）
# client.username_pw_set("myuser","mypassword")

# 連線至 MQTT 伺服器（伺服器位址,連接埠）
client.connect("127.0.0.1", 1883)

jsonData = json.dumps(facedevice_back)
client.publish("PublishTest", jsonData)


# # 建立連線（接收到 CONNACK）的回呼函數
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code " + str(rc))

#     # 每次連線之後，重新設定訂閱主題
#     client.subscribe("hello/world")

# # 接收訊息（接收到 PUBLISH）的回呼函數
# def on_message(client, userdata, msg):
#     # print("[{}]: {}".format(msg.topic, str(msg.payload)))
#     mqttMessage = msg.payload.decode('utf-8')
#     mqttMessage = json.loads(mqttMessage)
#     print(mqttMessage)

# # 設定建立連線回呼函數
# client.on_connect = on_connect

# # 設定接收訊息回呼函數
# client.on_message = on_message 

# client.subscribe("test_bind")

# # 進入無窮處理迴圈
# client.loop_forever()

