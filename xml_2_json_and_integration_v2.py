import xml.etree.ElementTree as ET
from datetime import datetime
# from collections import Counter, OrderedDict, namedtuple
import json
import time
import os
import re

######## integration example ########
'''
{
# id, 
*來源, (哪個專案 或 哪個公開資料集)
圖片名稱, 
匯入時間,  
*備註說明,"....…"
影像資訊:(width, height, depth),
object_detection:{物件名稱1:[{'xmin':1, 'ymin':2, 'xmax':3, 'ymax':4}, {'xmin':21, 'ymin':2, 'xmax':3, 'ymax':4}], 
                  物件名稱2: [{}....{}],
                  負樣本:[物件名稱6, 物件名稱10.....]},
segmentation_detection:{物件名稱a:[{points: [p1, p2 ,p3....]}],
                        物件名稱b:[...],
                        負樣本:[物件名稱z, 物件名稱x,...]},
classify:[類別1, 
          類別2],
pose_estimation:?
*face_recognition:{?},
}
'''
#####################

# xml folder path 
xml_init_path = "/home/eray/Documents/xml_2_json/20220428_小揚/xml"
xml_des_path = "/home/eray/Documents/xml_2_json/小揚_20220428_xml_2_json/personal_json"
   

# json file path (segment, pose, classify, face)
# segment_json = "/home/eray/Documents/xml_2_json/segment_pose_format/segmation/V_20210224_130854_EH0_00004.json"
# pose_json = "/home/eray/Documents/xml_2_json/segment_pose_format/骨架輸出格式參考/sep-json(每張照片一個jason)/p2.json"


######## define required argments ########
# 來源, (哪個專案 或 哪個公開資料集) and 備註說明
project_source = "台積電_事件偵測"    # ["台積電_環境物品", "台積電_事件偵測", "美光消防衣", "台積電_人身上的裝備"]
remark_description = "台積電_事件偵測拍攝的資料"     # ["台積電機器人拍攝的資料", "台積電_事件偵測拍攝的資料", "美光消防衣拍攝的資料", "台積電_人身上的裝備拍攝的資料"]


# 給全部出現樣本 -> 會自動產生負樣本
# total_sample = ['car_rear', 'clampOnRear', 'plateBig', 'plate', 'vergenceTube', 'person']
total_sample = ['person', 'ladder']
# total_sample = ['cones', 'fence', 'extinguisherCar', 'safeDoor', 'gutterHole', 'gutterCover', 'hydrant', 
#                 'redBox', 'extinguisher', 'extinguisher_error', 'safeDoor_open', 'cardClose', 'personFall', 
#                 'cones_error', 'capBlue', 'capWhite', 'capGreen', 'cardOpen', 'toolCabinet_open', 'cleaner', 'toolCabinet']



######## Don't change ########
# 定義json項目
json_category = ["source", "filename", "import_time", "remark", "size", "object_detection", "classify", 
                 "segmentation_detection", "pose_estimation", "face_recognition"]

# 定義第三層json項目
OD_category = ["負樣本"]

# 第一層自定義引數變量
set_arguments1 = [project_source, remark_description]

# 第三層自定義引數變量
set_arguments2 = [total_sample]


class ParseXML:
    def __init__(self, path, des_path):
        self.xml_path = path
        self.des_path = des_path
        self.layer1Keys = ["filename", "path", "size"]
        self.bndbox = ["xmin", "ymin", "xmax", "ymax"]
        self.layer1 = {}
        self.layer3 = {}
        self.obj_name = {}
        self.lost_elements = []
        self.no_obj_coord = []
        self.error_message = {"lost_elements": self.lost_elements, "no_obj_coord" : self.no_obj_coord}
        self.error_elements = []
        self.correct_param = []
        
    def parseTree(self):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        return root

    def iterTree(self):
        root = self.parseTree()
        pattern = re.compile(r"\s+")
        
        for i in self.layer1Keys[:-1]:
            try:
                _ = root.find(i).text
                    
            except AttributeError as e:
                # print(self.xml_path)
                self.lost_elements.append(self.xml_path)
                self.error_elements.append(i)
                continue

        # check xml layer1 elements is or not is exist
        print(f"Lost required elements: {self.error_elements}")

        size = root.find("size")
        img_size = tuple([i.text for i in size.iter() if not re.search(pattern, i.text)])
        
        if len(self.error_elements) > 0:
            for e in self.layer1Keys[:-1]:
                if e not in self.error_elements: 
                    self.correct_param.append(root.find(e).text)
            
            if self.layer1Keys[1] in self.error_elements:
                self.correct_param.append(os.path.join(self.des_path, root.find("filename").text))
                self.correct_param.append(img_size)
            else:
                self.correct_param.append(img_size)
        
            self.layer1 = {k:v for k, v in zip(self.layer1Keys, self.correct_param)}

        else:
            self.correct_param = [root.find("filename").text, os.path.join(self.des_path, root.find("filename").text), img_size]
            self.layer1 = {k:v for k, v in zip(self.layer1Keys, self.correct_param)}

        if root.find("object") is None:
            self.no_obj_coord.append(self.xml_path)

        else:
            for obj in root.iter("object"):
                name = obj.find("name").text
                if name not in self.obj_name.keys():
                    self.obj_name[name] = []

                bbox = obj.find("bndbox")
                box_val = [i.text for i in bbox.iter() if not re.search(pattern, i.text)]
                bndbox = {scope:val for scope, val in zip(self.bndbox, box_val)}
                self.obj_name[name].append(bndbox)

        self.layer3.update(self.obj_name)
        layers_param = (self.layer1, self.layer3, self.error_message)
            
        return layers_param
        

# layer1, layer3, error_message = ParseXML(xml_init_path, xml_des_path).iterTree()
# json_layer1 = json.dumps(layer1, ensure_ascii=False, indent=4)
# json_layer3 = json.dumps(layer3, ensure_ascii=False, indent=4)
# print(json_layer1, '\n', json_layer3)


class SetParamAndBuildJson():
    def __init__(self, set_category, set_args, xml_layers):  # counter
        jc, od = set_category
        (source, remark), total_sample = set_args

        # self.id = counter+1
        self.constructure = {}
        self.obj_detect = {}
        self.total_sample = total_sample[0]
        self.negative_sample = []
        self.time = datetime.now().isoformat(sep = " ", timespec = "seconds")
        
        # define category: obj_detect, segment_detect, pose_detect, classify
        self.category_layer1 = jc
        self.od_category = od[0] 
        # self.sd_category = od[:4] +["points"] + [od[6]] 
        # self.ps_category = [od[0]] + od[3:5] + ["joints"]
        # self.c_category = od[:2] + od[3:5]
        
        # define arguments: layer3_args
        self.source = source
        self.remark = remark
        
        # retrieve parsed xml layers 
        self.xml_layer1 = xml_layers[0]
        self.xml_layer3 = xml_layers[1]
        

    def build(self):
        layer1_keys = self.category_layer1[:6]
        layer1_vals = [self.source, self.xml_layer1["path"], self.time, 
                       self.remark, self.xml_layer1["size"], self.obj_detect]  # self.id
        
        for k, v in zip(layer1_keys, layer1_vals):
            self.constructure[k] = v

        for obj in self.total_sample:
            if obj not in self.xml_layer3.keys():
                self.negative_sample.append(obj)

        self.xml_layer3[self.od_category] = self.negative_sample
        self.obj_detect.update(self.xml_layer3)
        
        return self.constructure, self.obj_detect


    def to_json(self):
        Tree, _ = self.build()
        xml_2_json = json.dumps(Tree, ensure_ascii=False, indent=4)
        
        return xml_2_json


# treeLayer1, treeLayer3, error_message = ParseXML(xml_init_path, xml_des_path).iterTree()
# xml_to_json, _ = SetParamAndBuildJson((json_category, OD_category), (set_arguments1, set_arguments2), 
#                                       (treeLayer1, treeLayer3), 0).to_json()
# print(xml_to_json)


def save_2_json(xml_parser, path_in, path_out):
    fixed_path = re.split("/", path_in)[-1]
    complete_path = os.path.join(path_out, fixed_path[:-4]+".json")
    with open(complete_path , "w") as f:
        json.dump(xml_parser, f, ensure_ascii = False, indent=4)

    print(f"{fixed_path} -------------> {path_out}/{fixed_path[:-4]}.json \n")


def multi_xml_2_json(dir_path, output_path):
    not_xml_file = []
    not_read_parsed_text = []
    no_obj_coordinate = []
    count = 0
    pattern = re.compile(r".xml$")
    
    for xml_path in os.listdir(dir_path):
        if re.search(pattern, xml_path):
            treeLayer1, treeLayer3, error_message = ParseXML(os.path.join(dir_path, xml_path), output_path).iterTree()
            
            for idx, val in enumerate(error_message.values()):
                if idx < 1 and val != []:
                    not_read_parsed_text.append(val)
                if idx == 1 and val != []:
                    no_obj_coordinate.append(val) 
            
            xml_to_json, _ = SetParamAndBuildJson(set_category = (json_category, OD_category),
                                                  set_args = (set_arguments1, set_arguments2), 
                                                  xml_layers = (treeLayer1, treeLayer3)).build()   # counter = count
            save_2_json(xml_to_json, xml_path, output_path)
            count += 1
        
        else:
            not_xml_file.append(os.path.join(dir_path, xml_path))

    for num, obj in enumerate(no_obj_coordinate):
        if num < 5:
            print(f"{obj[0]} ----> xml沒有標示任何物件座標! <加入負樣本匯入!>")
    print(f"======== < {len(no_obj_coordinate)} > xml files not have any obj coordinate! <加入負樣本匯入!> ======== \n")
    
    for num, lost_obj in enumerate(not_read_parsed_text):
        if num < 5:
            print(f"{lost_obj[0]} ----> xml所需的元素不齊全!(ex: no <path> element) <已添加匯入!>")
    print(f"======== < {len(not_read_parsed_text)} > xml files missing required elements! <已添加匯入!> ======== \n")
    
    for num, not_xml in enumerate(not_xml_file):
        if num < 5:
            print(f"{not_xml} ------> not xml files!")
    print(f"======== < {len(not_xml_file)} > not xml files! <不匯入!> ======== \n")

    print(f"======== < {count} > xml files have been transformed to json! ======== \n")


if __name__ == "__main__":
    s = time.time()
    multi_xml_2_json(xml_init_path, xml_des_path)
    e = time.time()

    print(f"Spent {e-s:.2f} seconds!")



# class segment_integration():
#     def __init__(self, path, category, parameters):
#         param1, param2 = parameters
#         self.path = path
#         self.name = "segmentation_detection"
#         self.img_depth = 3
#         self.root = {self.name: {}}
#         self.category = category
#         self.source = param1[0]
#         self.descript = param1[1]
#         self.chi_name = param2[0]
#         self.style = param2[1]
#         self.scope = param2[2]
#         self.otherNotation = param2[3]
    
#     def retrieve_json(self):
#         with open(self.path, "r") as f:
#             data = json.load(f)
        
#         if "shapes" in data.keys():
#             data_param = data["shapes"]["label"], data["shapes"]["points"], data["imagePath"], data["imageHeight"], data["imageWidth"]
#             return data_param
#         else:
#             assert("not comform pattern !")

#     def constucture(self):
#         params = self.retrieve_json(self.path)

#         sd = [self.chi_name, self.style, self.scope, self.otherNotation]
#         sd_dict = {k:v for k, v in zip(self.category, sd+[params[2]]+[params[1]]+[])} 
#         sd_dict[""]
#         self.root[self.name].update({params[0]: [sd_dict]})
        

# def read_json(path):
#     with open(path, "r") as f:
#         data = json.load(f)

#     parse_json = json.dumps(data, indent=4)
#     print(parse_json)
#     return data

# parser = read_json(segment_json)
# print(parser["shapes"])