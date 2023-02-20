#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os, glob, time
import matplotlib.pyplot as plt

sourceVideo = "/home/eray/Documents/華夏_影片分段/Ch25_S-17/分割片段"
saveFolder = "/home/eray/Documents/華夏_影片分段/Ch25_S-17/影片切frame"
#sourceVideo = "/home/eray/Videos/"
#saveFolder = "/home/eray/Videos/"

# datetime = time.strftime('%Y%m%d_%H%M%S')
datetime = time.strftime('%Y%m%d')
counter = 100001
jumpFrame = 10

if __name__ == '__main__':

    listVideo = []
    listVideo += glob.glob(os.path.join(sourceVideo, "*.3gp"))
    listVideo += glob.glob(os.path.join(sourceVideo, "*.mkv"))
    listVideo += glob.glob(os.path.join(sourceVideo, "*.avi"))
    listVideo += glob.glob(os.path.join(sourceVideo, "*.mp4"))
    listVideo += glob.glob(os.path.join(sourceVideo, "*.MOV"))
    listVideo += glob.glob(os.path.join(sourceVideo, "*.MKV"))
    
    listVideo.sort()
    
    for i in range(len(listVideo)):
        # counter = 100001
        #baseName = datetime  #os.path.basename(listVideo[i])[:-4]
        cap = cv2.VideoCapture(listVideo[i])
        baseName = os.path.basename(listVideo[i])
        baseName = os.path.splitext(baseName)[0]
        ret, frame = cap.read()
        print (listVideo[i])

        while ret:
            print(baseName + '_' +str(counter)[1:]+'.jpg')
            cv2.imwrite(os.path.join(saveFolder, baseName + '_' +str(counter)[1:]+'.jpg'), frame)
            counter += jumpFrame
            
            for i in range(jumpFrame):
                ret, frame = cap.read()
            
    
