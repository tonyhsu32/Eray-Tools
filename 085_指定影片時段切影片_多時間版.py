# -*- coding: utf-8 -*- 
import cv2, os, glob, shutil
import numpy as np
import time
import ast


videoFilePath = r"C:\Users\eray\Desktop\裝備影機影片\video_already_cut\AI-VISION_192.168.100.167_0_20221020_050001.avi"
save_root = r'C:\Users\eray\Desktop\AI-VISION_ppe-collect\already_cut\AI-VISION_192.168.100.167_0_20221020_050001\20221020_050001_cut_fragment'
#cutSegment = [['04h00m30s', '04h01m13s']] #0581Q1

# 加入多時間片段
video_segment_path = r"C:\Users\eray\Desktop\AI-VISION_ppe-collect\already_cut\AI-VISION_192.168.100.167_0_20221020_050001\frame_to_time.txt"


def read_file(path):

    with open(path, "r") as f:
        frame_list = f.readlines()
    #print(type(ast.literal_eval(frame_list[0])))
    return ast.literal_eval(frame_list[0])


def getTime(vTime):
 
    h = int(vTime.partition("h")[0])
    m = int(vTime.partition("h")[2].partition("m")[0])
    s = int(vTime.partition("m")[2].partition("s")[0])
    return (h, m, s)
    
    
    
if __name__ == '__main__':
    
    # 加入多時間片段
    cutSegment = read_file(video_segment_path)
    print(len(cutSegment))
    
    videoFile = cv2.VideoCapture(videoFilePath)
    FPS = videoFile.get(cv2.CAP_PROP_FPS)
    vWidth, vHeight = (int(videoFile.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoFile.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    baseName = os.path.basename(videoFilePath)[:-4]
    
    (startH, startM, startS) = (0, 1, 0)    
    (endH, endM, endS) = (0, 2, 0)    
    
    beginFrame = FPS * (startH*3600 + startM*60 + startS)
    endFrame = FPS * (endH*3600 + endM*60 + endS)
    ''''
    for i in range(0, len(cutSegment)):
        (startH, startM, startS) = getTime(cutSegment[i][0])
        (endH, endM, endS) = getTime(cutSegment[i][1])
        beginFrame = FPS * (startH*3600 + startM*60 + startS) - 1
        endFrame = FPS * (endH*3600 + endM*60 + endS)
       
        save_name = os.path.join(save_root, baseName+"_"+str(i+1)+".mp4")
        print (save_name)
        videoFile.set(cv2.CAP_PROP_POS_FRAMES, beginFrame)  #設置起始的frame
        video_writer = cv2.VideoWriter(save_name, fourcc, FPS, (vWidth, vHeight))
        
        while beginFrame <= endFrame:
            ret, image = videoFile.read()
            video_writer.write(image)

            beginFrame += 1
            
        video_writer.release()
       '''

    
