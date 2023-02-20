from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pymongo import MongoClient, errors
from pymongo import InsertOne, UpdateOne, UpdateMany
from pymongo.errors import BulkWriteError, ConnectionFailure
from typing import List, Optional, Tuple
from Params_dataTypes import SearchParamModel
from collections import Counter
from enum import Enum
# from itertools import count
from bson import json_util
import json
import time
import sys
import os
import re
import gc


# 查詢物件：顯示公司現有資料的物件名稱、數量、定義與範例圖
# 查詢資料：用指定條件查詢（來源、物件項目、是否需確認過）。顯示圖片數量物件數量
# 匯出：用指定的條件（來源、物件項目、是否需確認過），將圖片與產生xml到指定的資料夾路徑 （圖片用軟連結）
# 匯入：工程師選擇好資料夾、輸入圖片的資訊、xml的類別名稱、範例圖片後，將此資料加入公司現有的資料管理中
# 新增類別：輸入物件名稱、label定義、上傳範例圖
# 修改類別：更新物件名稱、label定義、更新範例圖
# 修改訓練資料：指定修改物件名稱更動、匯入xml並指定類別修正


# app = FastAPI()

# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# define mongo client parameters
LOCALHOST = "127.0.0.1"  # "127.0.0.1", "192.168.33.157"
PORT = 27017
AUTH_USER = "root"
AUTH_PWD = "80661707"

DB_NAME = ["test_db", "obj_info_db"]   # test_db
DB_COLLECTION = ["test_data", "info_data"]   # test_data


# define search parameter
# PROJECT_SOURCE = "台積電_環境物品,台積電_事件偵測,美光消防衣,台積電_人身上的裝備"  # "台積電_巡檢", "奇美_槽車", "台積電_事件偵測"
PROJECT_SOURCE = "台積電_巡檢,台積電_事件偵測"
# PROJECT_SOURCE = ""

# LABEL_NAME = "cones,fence,capBlue,extinguisherCar,gutterHole,gutterCover,extinguisher_error\
#  redBox,extinguisher,cardClose,cones_error,cardOpen,cleaner,person,ladder,capBlue,capGreen,capWhite\
#  personFall,toolCabinet_open,toolCabinet,safeDoor,hydrant,safeDoor_open\
#  car_rear,clampOnRear,plateBig,plate,vergenceTube"
# LABEL_NAME = "cones,,,,,fence,,,,,capBlue,,,,,vergenceTube,,,,,person,,,,,plateBig,,,,,cleaner,,,,"
# LABEL_NAME = "cones,0,200,0,200,fence,0,200,0,200,capBlue,0,200,0,200,vergenceTube,,,,,person,,,,,plateBig,,,,,cleaner,,,,"
# LABEL_NAME = "cones,0,200,0,200,fence,0,200,0,200,capBlue,0,200,0,200" 
LABEL_NAME = "cones,,,,,fence,,,,,capBlue,,,,"
# LABEL_NAME = "cones,,,,"
# LABEL_NAME = ""

# DATA_TYPE = "object_detection,segment_detection,classify,pose_estimation,face_recognition"
# DATA_TYPE = "object_detection"
DATA_TYPE = ""

# RESOLUTION = "1280,1920,720,1080"   # "720,1280,480,720", "1280,1920,720,1080"
RESOLUTION = "" 

CONFIRM_OBJ = "1"  # 0
# CONFIRM_OBJ = "0"

CONFIRM_OBJ_AMOUNT = "4"
# CONFIRM_OBJ_AMOUNT = ""


class Mongo_Client:
    def __init__(self, host, port, db_name, db_collection, db_user, db_pwd):
        self.localhost = host
        self.port = port
        self.db_user = db_user
        self.db_pwd = db_pwd

        self.select_db = db_name
        self.db_collection = db_collection
       
    def set_db(self):
        try:
            param_wrap = {"host": self.localhost, 
                          "port": self.port,
                          "username": self.db_user, 
                          "password": self.db_pwd, 
                          # "authSource": "admin",
                          "authMechanism": 'SCRAM-SHA-1', # 'SCRAM-SHA-256'
                          }  # "serverSelectionTimeoutMS": 3000

            client = MongoClient(**param_wrap)
            print("Connected Mongodb client Success!")

        except ConnectionFailure as e:
            print(f"Mongodb Server Error: {e}")

        db = client[self.select_db] 
        db_col = db[self.db_collection]

        return db, db_col


class WrapMessage:
    def __init__(self, state, result):
        self.state = state
        self.result = result
        self.display_param = ["Total_Obj_Name", "Total_Source"]  # "全部資料物件數量"
        self.search_param = ["Match_Search_Obj_Data_and_Img_Amount", "Total_Search_Xml_Required_Data"]  # "儲存符合的圖片路徑", "計算搜尋出現的物件名稱", "統計搜尋重複出現的物件數量"
        
    def build_message(self, method):
        # wrap 
        if method == "display":
            wrap_message = {s_key: s_val for s_key, s_val in zip(self.display_param, self.result)}
        
        elif method == "search":
            wrap_message = {s_key: s_val for s_key, s_val in zip(self.search_param, self.result)}

        return {"code": self.state.value[0], "message": self.state.value[1], "results": wrap_message}


class Code_Status(Enum):
    NO_MATCH_DATA = (1, "無符合資料!")
    OK = (0, "成功!")
    FAILURE = (-1, "失敗!")


def SearchParams_trans_format(test_data):
    obj_bnd_list = {}
    group = 5
    
    # SearchParams
    # params = [test_data.source, test_data.label, test_data.type, test_data.resolution, test_data.confirm_obj, test_data.confirm_obj_amount]

    # test
    params = [*test_data]
        
    for idx, param in enumerate(params):
        # 解析label與範圍字串
        if idx == 1:
            for num in range(len(param.split(","))//5):
                obj_bnd_list[param.split(",")[group*num: group*(num+1)][0]] = param.split(",")[group*num: group*(num+1)][1:]
                    
            params[idx] = obj_bnd_list

        elif idx != 1:
            # print(param)
            if len(param.split(",")) > 1:
                params[idx] = param.split(",")
            else:
                params[idx] = [param]

    return params


# @app.get("/get_xml_data/")
def get_xml_data():
    fake_data = [
            ["/home/eray/Pictures/LOTUS_object_new/__00409.jpg",
                [
                    [
                        ["basket",["1056", "251", "1203", "384"]],
                        ["shop_cart",["576", "543", "827", "968"]],
                        ["person",["595", "34", "815", "436"]]
                    ],
                        ["1920", "1080", "3"],
                        ["台積電_環境物品"]
                    ]
                ]
            ,["/home/eray/Documents/LOTUS_object_datasets/train_data/object_train_2/2__00157.jpg",
                [
                    [
                        ["basket",["1086", "234", "1240", "330"]],
                        ["basket",["1151", "950", "1268", "1080"]],
                    ],
                        ["1920", "1080", "3"],
                        ["台積電_事件偵測"]
                    ]
                ]
            ]
    
    return fake_data

  
# db object unique (搜索全部出現物件名稱), amount (數量), definition (定義)
# @app.get("/display_obj/")
def db_display():
    obj_name, chi_obj_name = [], []

    _, db_collection = Mongo_Client(LOCALHOST, PORT, DB_NAME[1], DB_COLLECTION[1], AUTH_USER, AUTH_PWD).set_db()
    
    pipeline = [{"$match": {"$and": [
                               {"object_detection": {"$exists": True, "$ne": {}}}, 
                            ]
                        }},
                {"$project": {"_id": 0, 
                              "object_detection": 1, 
                            }
                        },
                ]

    try:
        cursor = db_collection.aggregate(pipeline, allowDiskUse=True)
    
        # 全部出現物件名稱, definition (定義)
        for doc in cursor:
            # print(doc, "\n")
            obj_name = list(doc["object_detection"].keys())
            
            for name in obj_name:
                for chi_key, chi_name in dict(doc["object_detection"][name]).items():
                    # 計算出現中文名稱
                    # print(chi_key, chi_name)
                    if chi_name not in chi_obj_name and chi_name != "" and chi_name != []:
                        chi_obj_name.append(chi_name)

        # print(obj_name)
        # print(chi_obj_name)

        total_obj_info = [f"{k+' ('+v})" for k, v in zip(obj_name, chi_obj_name)]

        source_txt = open("/home/eray/Documents/xml_2_json/mongo_db/source_cache")
        source = source_txt.read()
        # print(source[:-1].split(","))   

        source_txt.close()

        if doc == {}:
            status_msg = Code_Status.NO_MATCH_DATA
        else:
            status_msg = Code_Status.OK
        
        cursor.close()
        return WrapMessage(status_msg, [total_obj_info, source[:-1].split(",")]).build_message("display")  # amount
    
    except Exception as e:
        status_msg = Code_Status.FAILURE
        print(e)

    return {"code": status_msg.value[0], "message": status_msg.value[1], "results": "FAILURE !"}


# 搜索(指定條件查詢) ex: 來源、物件項目(只有包含這個物件-[1 or 2物件以上]). 顯示圖片數量、物件數量obj: [{xmin: ..., xmax, ymin, ymax}, {}, {}...]
# 查詢相關來源、物件項目(相依專案會用到)  
#@app.post("/search_obj/")
def db_search(test_data):  # --> test
#def db_search(SearchParams: Optional[SearchParamModel] = None):
    # obj boundary filter
    # print(SearchParams)
    bnd_filter_1, bnd_filter_2  = [], []
    conform_obj_bnd_filter = {}
    
    # pipeline data limit
    # num = 100
  
    _, db_collection = Mongo_Client(LOCALHOST, PORT, DB_NAME[0], DB_COLLECTION[0], AUTH_USER, AUTH_PWD).set_db()

    # trans_format
    parameters = SearchParams_trans_format(test_data)
    
    source_param = parameters[0]
    label_param = parameters[1]
    type_param = parameters[2]
    resolution_param = parameters[3]
    confirm_sample = parameters[4]
    confirm_sample_amount = parameters[5]
    

    # inititalize pipeline
    or_pipe = {"$or": []}
    and_pipe = {"$and": []}

    pipeline = [{"$match": 
                    {}
                },
                # {"$limit": num},
                {"$project": 
                    {
                        "_id": 1, 
                        "source": 1, 
                        "remark": 1,
                        "filename": 1,
                        "size": 1,
                    }
                }]


    # Search codition
    # add multi filters in pipline

    # 判斷有無開「確認圖片正負樣本有無搜索的物件」的功能，有的話在pipeline裡的$match字典生成($or指令字典)，反之跳過
    if eval(confirm_sample[0]):
        if label_param != {}:
            if len(list(label_param.keys())):
                # 正樣本搜索 (在$or指令字典加入物件搜索)
                label_name_filter = [{f"object_detection.{obj}": {"$exists": True, "$ne": []}} for obj in list(label_param.keys())]
                or_pipe["$or"].extend(label_name_filter)

                # 負樣本搜索 (在$or指令字典加入物件搜索)
                negative_sample_filter = {"object_detection.負樣本": { 
                                            "$in": list(label_param.keys())}}

                or_pipe["$or"].append(negative_sample_filter)
                pipeline[0]["$match"] = or_pipe

                # (全部搜索物件與正樣本)取差集，(全部搜索物件與負樣本)取差集，兩個差集取交集就是正負樣本都沒有搜索到的物件
                not_confirm_sample_filter = {"not_confirm_positive_sample": {
                                                "$setDifference": [list(label_param.keys()), ["$object_detection.k"]]
                                                },
                    
                                             "not_confirm_negative_sample": {
                                                "$setDifference": [list(label_param.keys()), "$object_detection.負樣本"]
                                                },

                                             "not_confirm_sample": {
                                                "$setIntersection": [
                                                    {"$setDifference": [list(label_param.keys()), ["$object_detection.k"]]},
                                                    {"$setDifference": [list(label_param.keys()), "$object_detection.負樣本"]}
                                                ]
                                            },

                                             "not_confirm_sample_size": {
                                                "$size": {
                                                    "$setIntersection": [
                                                        {"$setDifference": [list(label_param.keys()), ["$object_detection.k"]]},
                                                        {"$setDifference": [list(label_param.keys()), "$object_detection.負樣本"]}
                                                    ]
                                                }},
                                            }

                pipeline[1]["$project"].update(not_confirm_sample_filter)
        else:
            print("使用「確認圖片正負樣本有無搜索物件」的功能，搜索物件不能為空！")
            
    else:
        # 沒有開「確認圖片正負樣本有無搜索物件」的功能，在pipeline的$match字典中加入(包含全部搜索物件的$and字典)
        if label_param != {}:
            if len(list(label_param.keys())):
                label_name_filter = [{f"object_detection.{obj}": {"$exists": True, "$ne": []}} for obj in list(label_param.keys())]
                and_pipe["$and"].extend(label_name_filter)
                pipeline[0]["$match"] = and_pipe
            

    # 判斷pipeline裡的$match字典有or或and指令，加入相應的(資料類型參數)       
    if "$and" in pipeline[0]["$match"].keys() or pipeline[0]["$match"] == {}:
        if len(type_param[0]) > 0 and type_param[0] != "":
            type_filter = [{t_param: {"$exists": True, "$ne": {}}} for t_param in type_param]
            and_pipe["$and"].extend(type_filter)
            pipeline[0]["$match"] = and_pipe

            # define $project obj_filter
            project_type_filter = {type: 1 for type in type_param}
            pipeline[1]["$project"].update(project_type_filter)

        else:
            # define $project obj_filter
            # project_type_filter = {type: 1 for type in type_param}
            pipeline[1]["$project"].update({"object_detection": 1})
    
    elif "$or" in pipeline[0]["$match"].keys():
        if len(type_param[0]) > 0 and type_param[0] != "":
            type_filter = [{t_param: {"$exists": True, "$ne": {}}} for t_param in type_param]
            and_pipe["$and"].extend(type_filter)
            pipeline[0]["$match"] = and_pipe

            # define $project obj_filter
            project_type_filter = {type: 1 for type in type_param}
            pipeline[1]["$project"].update(project_type_filter)

        else:
            # define $project obj_filter
            # project_type_filter = {type: 1 for type in type_param}
            pipeline[1]["$project"].update({"object_detection": 1})

    
    # 判斷pipeline裡的$match字典有or或and指令，加入相應的(來源參數) ex: 開「確認圖片正負樣本有無搜索物件」的功能時，多來源使用or指令，反之相反
    if "$or" in pipeline[0]["$match"].keys():
        if len(source_param[0]) > 0 and source_param[0] != "": 
            source_filter = [{"source": s_param} for s_param in source_param]

            or_pipe["$or"].extend(source_filter)
            pipeline[0]["$match"] = or_pipe

    elif "$and" in pipeline[0]["$match"].keys():
        if len(source_param[0]) > 0 and source_param[0] != "": 
            source_filter = [{"source": s_param} for s_param in source_param]

            or_pipe["$or"].extend(source_filter)
            and_pipe["$and"].append(or_pipe)
        
    elif len(source_param[0]) > 0 and source_param[0] != "": 
        source_filter = [{"source": s_param} for s_param in source_param]

        or_pipe["$or"].extend(source_filter)
        pipeline[0]["$match"] = or_pipe

    
    # 建立解析度範圍的篩選器，加入初始的aggregate pipeline filter中
    if resolution_param != [""]:
        size_cond = {"size": {"$exists": True, "$ne": {}}}
        and_pipe["$and"].append(size_cond)
        pipeline[0]["$match"] = and_pipe

        # conform_resolution = {"size_filter": {}}
        # size_filter = {"$filter": {
        #                     "input": "$size", 
        #                     "as": "item", 
        #                     "cond": {}
        #                     }
        #                 }

        # # "1280,1920,720,1080"
        # size_filter_2 = {"$and": [
        #                     {"$gte": [int(resolution_param[0]), {"$toInt": "$$item.0"}]},
        #                     {"$lte": [{"$toInt": "$$item.0"}, int(resolution_param[1])]},  
        #                     {"$gte": [int(resolution_param[2]), {"$toInt": "$$item.1"}]},  
        #                     {"$lte": [{"$toInt": "$$item.1"}, int(resolution_param[3])]},
        #                 ]}

        # size_filter["$filter"]["cond"].update(size_filter_2) 
        # conform_resolution["size_filter"].update(size_filter)

        # pipeline[1]["$project"].update(conform_resolution)

    
    # 為每一個搜尋物件，建立物件長寬的篩選器，加入初始的aggregate pipeline filter中
    if len(label_param.keys()) > 0:
        for loc, label in enumerate(list(label_param.keys())):
            if list(label_param.values())[loc][0] != "":
                bnd_filter_1.append({"$filter": {
                                        "input": f"$object_detection.{label}", 
                                        "as": "item", 
                                        "cond": {}
                                    }
                                })
                conform_obj_bnd_filter.update({f"conform_obj_scope_{label}": ""})
        # print(bnd_filter_1)
        # print(conform_obj_bnd_filter)
    
        for bnd in list(label_param.values()):
            if bnd[0] != "":
                bnd_filter_2.append({"$and": [
                                        {"$lte": [{"$subtract": [{"$toInt": "$$item.xmax"}, {"$toInt": "$$item.xmin"}]}, int(bnd[1]) - int(bnd[0])]},
                                        {"$lte": [{"$subtract": [{"$toInt": "$$item.ymax"}, {"$toInt": "$$item.ymin"}]}, int(bnd[3]) - int(bnd[2])]},
                                    ]})
        # print(bnd_filter_2)

        for obj_filter, filter1, filter2 in zip(conform_obj_bnd_filter, bnd_filter_1, bnd_filter_2):
            filter1["$filter"]["cond"] = filter2
            # print(obj_filter)
            conform_obj_bnd_filter[obj_filter] = filter1

        # print(json.dumps(conform_obj_bnd_filter, ensure_ascii=False, indent=4))
        pipeline[1]["$project"].update(conform_obj_bnd_filter)


    # show pipeline
    print(f"pipeline:\n{json.dumps(pipeline, ensure_ascii=False, indent=4)}")

    try:
        cursor = db_collection.aggregate(pipeline, allowDiskUse=True)
        
        # 正負樣本名稱，物件數量
        obj_name, total_obj = [], []

        # 解析度，物件圖片範圍計數器
        doc_amount, resolution_amount, scope_counter, param_counter = 0, 0, 0, 0
        # calculate_obj_amount = Counter()

        # 物件正負樣本確認
        not_confirm_counter = 0
        # doc_id = []

        # xml所需物件資訊儲存
        retrieve_xml_data, res_xml_data, bnd_xml_data, not_confirm_xml_data = [], [], [], []

        
        # resolution comparator
        res_filter_1 = lambda x: True if int(resolution_param[0]) <= int(x) <= int(resolution_param[1]) else False
        res_filter_2 = lambda y: True if int(resolution_param[2]) <= int(y) <= int(resolution_param[3]) else False
        

        # 計算全部資料, img amount (圖片數量)
        for doc in cursor:
            # 儲存搜索資料
            xml_data, content = [], []

            for obj, bnd in doc["object_detection"].items():
                if obj != "負樣本":
                    bnd_data = [[] for i in range(len(bnd))]

                    for num, data in enumerate(bnd):
                        bnd_data[num].extend(list(data.values()))

                    bnd_data.insert(0, obj)
                    # print(bnd_data, "\n")

                    content.append(list(bnd_data))

            xml_data.append(doc["filename"].split("/")[-1])
            content.append([[doc["source"]], doc["size"]])
            xml_data.append(content)
            print(xml_data, "\n")

            retrieve_xml_data.append(xml_data)

            param_status_counter = 0

            # resolution method:
            if resolution_param != [""]:
                if res_filter_1(doc["size"][0]) and res_filter_2(doc["size"][1]):
                    # print(doc, "\n")

                    # 儲存搜索資料
                    xml_data, content = [], []

                    for obj, bnd in doc["object_detection"].items():
                        if obj != "負樣本":
                            bnd_data = [[] for i in range(len(bnd))]

                            for num, data in enumerate(bnd):
                                bnd_data[num].extend(list(data.values()))

                            bnd_data.insert(0, obj)
                            # print(bnd_data, "\n")

                            content.append(list(bnd_data))

                    xml_data.append(doc["filename"].split("/")[-1])
                    content.append([[doc["source"]], doc["size"]])
                    xml_data.append(content)
                    print(xml_data, "\n")

                    res_xml_data.append(xml_data)

                    resolution_amount += 1

                    # resolution + (difference + not obj_scope) method:
                    if eval(confirm_sample[0]) and conform_obj_bnd_filter == {}:
                        # 開「確認圖片正負樣本有無搜索物件」的功能 -> difference
                        if len(set(label_param.keys()).difference(set(list(doc["object_detection"].keys())[:-1] + doc["object_detection"]["負樣本"]))) <= int(confirm_sample_amount[0]):
                            # print(doc, "\n")

                            # 儲存搜索資料
                            xml_data, content = [], []

                            for obj, bnd in doc["object_detection"].items():
                                if obj != "負樣本":
                                    bnd_data = [[] for i in range(len(bnd))]

                                    for num, data in enumerate(bnd):
                                        bnd_data[num].extend(list(data.values()))

                                    bnd_data.insert(0, obj)
                                    # print(bnd_data, "\n")

                                    content.append(list(bnd_data))

                            xml_data.append(doc["filename"].split("/")[-1])
                            content.append([[doc["source"]], doc["size"]])
                            xml_data.append(content)
                            print(xml_data, "\n")

                            not_confirm_xml_data.append(xml_data)

                            # doc_id.append(doc["_id"])

                            not_confirm_counter += 1

                    # resolution + (obj_scope + not difference) method:
                    elif conform_obj_bnd_filter != {} and not eval(confirm_sample[0]):  
                        for param in list(conform_obj_bnd_filter.keys()):
                            # print(param)
                            # print(doc[param])
                            if doc[param] != None and len(doc[param]) > 0:
                                # param_counter += 1
                                # print(f"num_{param_counter} {param}: ", doc[param])
                                param_status_counter += 1
                                # print(param_status_counter)
                                if param_status_counter == len(list(conform_obj_bnd_filter.keys())): 
                                    # 儲存搜索資料 
                                    xml_data, content = [], []

                                    for obj, bnd in doc["object_detection"].items():
                                        if obj != "負樣本":
                                            bnd_data = [[] for i in range(len(bnd))]

                                            for num, data in enumerate(bnd):
                                                bnd_data[num].extend(list(data.values()))

                                            bnd_data.insert(0, obj)
                                            # print(bnd_data, "\n")

                                            content.append(list(bnd_data))

                                    xml_data.append(doc["filename"].split("/")[-1])
                                    content.append([[doc["source"]], doc["size"]])
                                    xml_data.append(content)
                                    print(xml_data, "\n")

                                    bnd_xml_data.append(xml_data)

                                    scope_counter += 1

                                else:
                                    scope_counter += 0

                    # resolution + (obj_scope + difference) method:
                    elif conform_obj_bnd_filter != {} and eval(confirm_sample[0]):
                        # 開「確認圖片正負樣本有無搜索物件」的功能 -> difference
                        if len(set(label_param.keys()).difference(set(list(doc["object_detection"].keys())[:-1] + doc["object_detection"]["負樣本"]))) == int(confirm_sample_amount[0]):
                            # print(doc, "\n")
                            for param in list(conform_obj_bnd_filter.keys()):
                                if doc[param] != None and len(doc[param]) > 0:
                                    # param_counter += 1
                                    # print(f"num_{param_counter} {param}: ", doc[param])
                                    param_status_counter += 1
                                    # print(param_status_counter)
                                    if param_status_counter == len(list(conform_obj_bnd_filter.keys())):
                                        # print(doc, "\n")
                                        xml_data, content = [], []

                                        for obj, bnd in doc["object_detection"].items():
                                            if obj != "負樣本":
                                                bnd_data = [[] for i in range(len(bnd))]

                                                for num, data in enumerate(bnd):
                                                    bnd_data[num].extend(list(data.values()))

                                                bnd_data.insert(0, obj)
                                                # print(bnd_data, "\n")

                                                content.append(list(bnd_data))

                                        xml_data.append(doc["filename"].split("/")[-1])
                                        content.append([[doc["source"]], doc["size"]])
                                        xml_data.append(content)
                                        print(xml_data, "\n")

                                        bnd_xml_data.append(xml_data)

                                        # doc_id.append(doc["_id"])
                                        
                                        scope_counter += 1

                                    else:
                                        scope_counter += 0 

            else:
                # print(doc, "\n")

                # 儲存搜索資料
                xml_data, content = [], []

                for obj, bnd in doc["object_detection"].items():
                    if obj != "負樣本":
                        bnd_data = [[] for i in range(len(bnd))]

                        for num, data in enumerate(bnd):
                            bnd_data[num].extend(list(data.values()))

                        bnd_data.insert(0, obj)
                        print(bnd_data, "\n")

                        content.append(list(bnd_data))

                xml_data.append(doc["filename"].split("/")[-1])
                content.append([[doc["source"]], doc["size"]])
                xml_data.append(content)
                print(xml_data, "\n")

                retrieve_xml_data.append(xml_data)

                doc_amount += 1

                # difference + not obj_scope method
                if eval(confirm_sample[0]) and conform_obj_bnd_filter == {}:
                    # 開「確認圖片正負樣本有無搜索物件」的功能 -> difference
                    if len(set(label_param.keys()).difference(set(list(doc["object_detection"].keys())[:-1] + doc["object_detection"]["負樣本"]))) == int(confirm_sample_amount[0]):
                        # print(doc, "\n")

                        # 儲存搜索資料
                        xml_data, content = [], []

                        for obj, bnd in doc["object_detection"].items():
                            if obj != "負樣本":
                                bnd_data = [[] for i in range(len(bnd))]

                                for num, data in enumerate(bnd):
                                    bnd_data[num].extend(list(data.values()))

                                bnd_data.insert(0, obj)
                                # print(bnd_data, "\n")

                                content.append(list(bnd_data))

                        xml_data.append(doc["filename"].split("/")[-1])
                        content.append([[doc["source"]], doc["size"]])
                        xml_data.append(content)
                        print(xml_data, "\n")

                        not_confirm_xml_data.append(xml_data)

                        # doc_id.append(doc["_id"])

                        not_confirm_counter += 1

                # obj_scope + not difference method:
                elif conform_obj_bnd_filter != {} and not eval(confirm_sample[0]):  
                    for param in list(conform_obj_bnd_filter.keys()):
                        # print(param)
                        # print(doc[param])
                        if doc[param] != None and len(doc[param]) > 0:
                            # param_counter += 1
                            # print(f"num_{param_counter} {param}: ", doc[param])
                            param_status_counter += 1
                            # print(param_status_counter)
                            if param_status_counter == len(list(conform_obj_bnd_filter.keys())):
                                # 儲存搜索資料
                                xml_data, content = [], []

                                for obj, bnd in doc["object_detection"].items():
                                    if obj != "負樣本":
                                        bnd_data = [[] for i in range(len(bnd))]

                                        for num, data in enumerate(bnd):
                                            bnd_data[num].extend(list(data.values()))

                                        bnd_data.insert(0, obj)
                                        # print(bnd_data, "\n")

                                        content.append(list(bnd_data))

                                xml_data.append(doc["filename"].split("/")[-1])
                                content.append([[doc["source"]], doc["size"]])
                                xml_data.append(content)
                                print(xml_data, "\n")

                                bnd_xml_data.append(xml_data)

                                scope_counter += 1

                            else:
                                scope_counter += 0

                # obj_scope + difference method:
                elif conform_obj_bnd_filter != {} and eval(confirm_sample[0]):
                    # 開「確認圖片正負樣本有無搜索物件」的功能 -> difference
                    if len(set(label_param.keys()).difference(set(list(doc["object_detection"].keys())[:-1] + doc["object_detection"]["負樣本"]))) == int(confirm_sample_amount[0]):
                        # print(doc, "\n")
                        for param in list(conform_obj_bnd_filter.keys()):
                            if doc[param] != None and len(doc[param]) > 0:
                                # param_counter += 1
                                # print(f"num_{param_counter} {param}: ", doc[param])
                                param_status_counter += 1
                                # print(param_status_counter)
                                if param_status_counter == len(list(conform_obj_bnd_filter.keys())):
                                    # print(doc, "\n")

                                    # 儲存搜索資料
                                    xml_data, content = [], []

                                    for obj, bnd in doc["object_detection"].items():
                                        if obj != "負樣本":
                                            bnd_data = [[] for i in range(len(bnd))]

                                            for num, data in enumerate(bnd):
                                                bnd_data[num].extend(list(data.values()))

                                            bnd_data.insert(0, obj)
                                            # print(bnd_data, "\n")

                                            content.append(list(bnd_data))

                                    xml_data.append(doc["filename"].split("/")[-1])
                                    content.append([[doc["source"]], doc["size"]])
                                    xml_data.append(content)
                                    print(xml_data, "\n")

                                    bnd_xml_data.append(xml_data)

                                    # doc_id.append(doc["_id"])
                                    
                                    scope_counter += 1

                                else:
                                    scope_counter += 0  


        # finall counter output (優先順序從上到下) -> 比較解析度、物件範圍、確認圖片正負樣本有無搜索物件
        if resolution_param != [""] and conform_obj_bnd_filter != {} and eval(confirm_sample[0]):
            output_counter = scope_counter
            total_xml_data = bnd_xml_data

        elif resolution_param != [""] and eval(confirm_sample[0]):
            output_counter = not_confirm_counter
            total_xml_data = not_confirm_xml_data

        elif resolution_param != [""] and conform_obj_bnd_filter != {}:
            output_counter = scope_counter
            total_xml_data = bnd_xml_data

        elif eval(confirm_sample[0]):
            output_counter = not_confirm_counter
            total_xml_data = not_confirm_xml_data

        elif conform_obj_bnd_filter != {}:
            output_counter = scope_counter
            total_xml_data = bnd_xml_data

        elif resolution_param != [""]:
            output_counter = resolution_amount
            total_xml_data = res_xml_data

        else: 
            output_counter = doc_amount
            total_xml_data = retrieve_xml_data

        # determine whether the search function has data
        if output_counter == 0:
            status_msg = Code_Status.NO_MATCH_DATA
        else:
            status_msg = Code_Status.OK
    
        cursor.close()
        return WrapMessage(status_msg, [output_counter, total_xml_data]).build_message("search") 

    except Exception as e:
        status_msg = Code_Status.FAILURE
        print(e)
        
    return {"code": status_msg.value[0], "message": status_msg.value[1], "results": "FAILURE !"}


if __name__ == "__main__":
   
    #uvicorn.run(app=app, host='0.0.0.0', port=8080, debug=True)
    
    s = time.time()

    # db object unique (搜索全部出現物件名稱), amount (數量), definition (定義)
    # display_status_msg = db_display()

    # print(display_status_msg['code'])
    # print(display_status_msg['message'])
    # print(json.dumps(display_status_msg['result'], ensure_ascii = False, indent=4))

    
    # 搜索(指定條件查詢) ex: 來源、物件項目、圖片數量、物件數量
    data = (PROJECT_SOURCE, LABEL_NAME, DATA_TYPE[:16], RESOLUTION, CONFIRM_OBJ, CONFIRM_OBJ_AMOUNT)  # LABEL_NAME[:19], CONFIRM_OBJ
    
    # trans_format = SearchParams_trans_format(data)
    # print("source_param: {0}\nlabel_param: {1}\ntype_param: {2}\nresolution: {3}\nconfirm_sample: {4}".format(*tuple(trans_format)))

    search_status_msg = db_search(data)
    
    print(search_status_msg['code'])
    print(search_status_msg['message'])
    print(json.dumps(search_status_msg['results'], ensure_ascii = False, indent=4))

    e = time.time()
    print(f"Spent {e-s:.2f} seconds!")


