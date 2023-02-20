# 訂閱者（subscriber）指令稿 subscriber1.py
import json
import paho.mqtt.client as mqtt

# 建立連線（接收到 CONNACK）的回呼函數
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # 每次連線之後，重新設定訂閱主題
    client.subscribe("hello/world")

# 接收訊息（接收到 PUBLISH）的回呼函數
def on_message(client, userdata, msg):
    # print("[{}]: {}".format(msg.topic, str(msg.payload)))
    mqttMessage = msg.payload.decode('utf-8')
    mqttMessage = json.loads(mqttMessage)
    print(mqttMessage)

# 建立 MQTT Client 物件
client = mqtt.Client()

# 設定建立連線回呼函數
client.on_connect = on_connect

# 設定接收訊息回呼函數
client.on_message = on_message

# 設定登入帳號密碼（若無則可省略）
# client.username_pw_set("myuser","mypassword")

if client.on_message != "":
    # 連線至 MQTT 伺服器（伺服器位址,連接埠）
    client.connect("127.0.0.1", 1883)

    device_back = {
        "code": "",
        "msg": "",
        "device_id": "7101389947744",
        "dev_cur_pts": 1584053128,
        "tag": "platfrom define",       
        "datas":
            {       
                "device_token": ""
            }
    }

    jsonData = json.dumps(device_back)
    client.publish("test_bind", jsonData)
    
    client.loop_stop()

    # 進入無窮處理迴圈
    # client.loop_forever()