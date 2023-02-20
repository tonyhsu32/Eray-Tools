from typing import List, Optional, Tuple, Dict, Union
from pydantic import BaseModel


# define search parameters
PROJECT_SOURCE = "台積電_環境物品,台積電_事件偵測,美光消防衣,台積電_人身上的裝備"  # 台積電_巡檢
LABEL_NAME = "cones,fence,capBlue,extinguisherCar,gutterHole,gutterCover,extinguisher_error,\
 redBox,extinguisher,cardClose,cones_error,cardOpen,cleaner,person,ladder,capBlue,capGreen,capWhite,\
 personFall,toolCabinet_open,toolCabinet,safeDoor,hydrant,safeDoor_open,\
 car_rear,clampOnRear,plateBig,plate,vergenceTube"

LABEL_NAME = "cones,0,200,0,200,fence,0,200,0,200,capBlue,0,200,0,200" 
# LABEL_NAME = "cones,600,500,1000,1000,fence,,,,,capBlue,,,,"
# LABEL_NAME = "cones,,,,"
# LABEL_NAME = ""

DATA_TYPE = "object_detection,segment_detection,classify,pose_estimation,face_recognition"
# DATA_TYPE = ""

RESOLUTION = "1280,1920,720,1080"   # "720,1280,480,720", "1280,1920,720,1080"
# RESOLUTION = ""

CONFIRM_OBJ = "1"  # 0
# CONFIRM_OBJ = "" 

CONFIRM_OBJ_AMOUNT = "4"


class SearchParamModel(BaseModel):
    source: str
    label: str
    type: str
    resolution: str
    confirm_obj: str
    confirm_obj_amount: str


    def SearchParams_trans_format(self):
        # resolution_list = []
        obj_bnd_list = {}
        params = [self.source, self.label, self.type, self.resolution, self.confirm_obj, self.confirm_obj_amount]  
        group = 5
        
        for idx, param in enumerate(params):
            if idx == 1:
                for num in range(len(param.split(","))//5):
                    obj_bnd_list[param.split(",")[group*num: group*(num+1)][0]] = param.split(",")[group*num: group*(num+1)][1:]
                    
                params[idx] = obj_bnd_list

            elif idx != 1:
                if len(param.split(",")) > 1:
                    params[idx] = param.split(",")
                else:
                    params[idx] = [param]

        return params
        

if __name__ == "__main__":

    test_params = SearchParamModel(source = PROJECT_SOURCE,
                                   label = LABEL_NAME,
                                   type = DATA_TYPE[:16],
                                   resolution = RESOLUTION, 
                                   confirm_obj = CONFIRM_OBJ,
                                   confirm_obj_amount = CONFIRM_OBJ_AMOUNT).SearchParams_trans_format()  # label = LABEL_NAME[:19]
                                
    print("source_param: {0}\nlabel_param: {1}\ntype_param: {2}\nresolution: {3}\nconfirm_obj: {4}\nconfirm_obj_amount: {5}".format(*tuple(test_params))) 
  

