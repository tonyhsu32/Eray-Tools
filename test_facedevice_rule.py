# Face Device protocol communication format
# - Personnel information management

# Initialize parameter
mqtt_cmd = (1, 2)
mqtt_operate_id = [i for i in range(1, 11)].remove(5)
piclib_manage = list(range(0, 7))

platform_send_no_param = {
    "mqtt_cmd": "",
    "mqtt_operate_id": "",
    "device_token": "",
    "device_id": "",
    "tag": "platfrom define",
    "piclib_manage": "",
}

# - code 0: configuration succeeded, -1: configuration failed.
code = (0, -1)
msg = list()
device_back_no_datas = {
    "code": 0,
    "msg": "download PicLib status",
    "device_id": "7101389947744",
    "dev_cur_pts": 1583986208,
    "tag": "platfrom define",
}


# status 0: Add single or multiple - device back no failure
# - platform send
add_msg = "download PicLib status"

# - platform send
add_param_init = {
    "param":
        {
            "lib_name": "Smart Park",
            "lib_id": "8",
            "server_ip": "172.18.195.61",
            "server_port": 80,
            "pictures":
                [{
                    "active_time": "2020/01/1 00:00:01",
                    "user_id": "11",
                    "user_name": "Zhang San",
                    "end_time": "2020/12/30 23:59:59",
                    "p_id": "null",
                    "picture": "/192952.JPG"
                }]
        }
}

# - device back
add_data = {
    "datas":
        [{
            "pic_url": "/192952.JPG",
            "picture_statues": 10,  # status 10: download succeed, 20: download failed
            "user_id": "11"
        },
        {
            "pic_url": "/linxiaofei.jpg",
            "picture_statues": 10,
            "user_id": "22"
        }]
}

# status 1: Delete all photo
# - platform send
delete_all_piclib = 1
delete_all_msg = {"success": "delete all piclib success!", "failure": "mqtt param erro!"}


# status 2: Delete batch
# - platform send
delete_batch_piclib = 2
delete_batch_msg = {"success": "delete all piclib success!", "failure": "mqtt param erro!"}

# - platform send
delete_batch_param_init = {
    "param":{
        "lib":[
            {
                "lib_id": "8"
            },
            {
                "lib_id": "9"
            }
        ]
    }
}

# status 3: delete individual or multiple
# - platform send
delete_batch_piclib = 3
delete_individua_msg = {"success": "delete users piclib success"}

delete_individual_data_init = {
    "datas":[
        {
            "user_id": "11",
            "status": 0  # status 0: delete success, 1: delete failure
        },
        {
            "user_id": "22",
            "status": 0
        }
    ]
}

# status 4: query all face
# - platform send
delete_batch_piclib = 4
page = 0  # (0, -1, n)  # queries the total number: -1, n pages of n query: n, the first page will fill 0: 0

# - device back
query_all_msg = "mqtt query success!"

# page = -1
query_all_neg_page_init = {
    "datas":{
        "total_num": 30102
    }
}

# page = 2
query_all_n_page_init = {
    "datas":[
        {
            "lib_id": "8",
            "lib_name": "Smart Park",
            "user_id": "1",
            "user_name": "Zhang San",
            "active_time": "2020/01/1 00:00:01",
            "end_time": "2020/12/30 23:59:59",
        },
        {
            "lib_id": "9",
            "lib_name": "Smart Park",
            "user_id": "2",
            "user_name": "Li Si",
            "active_time": "2020/01/1 00:00:01",
            "end_time": "2020/12/30 23:59:59",
        }
    ]
}


# status 5: query batch
# - platform send
delete_batch_piclib = 5
query_batch_msg = "mqtt query success!"

query_batch_param_init = {
    "param":{
        "lib":[
            {
                "lib_id": "8"
            },
            {
                "lib_id": "9"
            }
        ]
    }
}

# - device back
query_batch_data_init = {
    "datas":[
        {
            "lib_id": "8",
            "lib_name": "Smart Park",
            "user_id": "1",
            "user_name": "Zhang San",
            "active_time": "2020/01/1 00:00:01",
            "end_time": "2020/12/30 23:59:59",
        },
        {
            "lib_id": "9",
            "lib_name": "Smart Park",
            "user_id": "2",
            "user_name": "Li Si",
            "active_time": "2020/01/1 00:00:01",
            "end_time": "2020/12/30 23:59:59",
        }
    ]
}

# status 6: query individual or multiple
query_individual_piclib = 6
query_individual_msg = "mqtt query success!"

# - platform send
query_individual_param_init = {
    "users":[
        {
            "user_id": "1"
        },
        {
            "user_id": "2"
        }
    ]
}

# - device back
query_individual_data_init = {
    "datas":[
        {
            "lib_id": "8",
            "lib_name": "intelligent park",
            "user_id": "1",
            "user_name": "Zhang San",
            "active_time": "2020/01/1 00:00:01",
            "end_time": "2020/12/30 23:59:59",
        },
        {
            "lib_id": "9",
            "lib_name": "intelligent park",
            "user_id": "2",
            "user_name": "Li Si",
            "active_time": "2020/01/1 00:00:01",
            "end_time": "2020/12/30 23:59:59",
        }
    ]
}

# MQTT bind and undind device operation
# - platform send
bind_ctrl = (0, 1)
init_status = {
    "mqtt_cmd": 1,
    "mqtt_operate_id": 10,
    "device_id": "7101389947741",
    "tag": "platfrom define",
    "bind_ctrl": ""
}

bind = init_status["bind_ctrl"] = bind_ctrl[0]
unbind = init_status["bind_ctrl"] = bind_ctrl[1]

# -device back
bind_code = (0, -1)
bind_msg = {"success": "mqtt bind ctrl success", "failure": "The device has been bound! ip:192.168.1.88 platfrom:2"}
bind_datas = {"success": {"datas": {"device_token": "1057628122"}},
              "failure": {"datas": "nodata"}}

unbind_msg = {"success": "mqtt unbind ctrl success", "failure": "device_token erro!"}
undind_datas = {"success": {"datas": "nodata"},
                "failure": {"datas": "nodata"}}

bind_status = {
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

