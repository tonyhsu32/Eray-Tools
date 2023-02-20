# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os, glob, time, math

sourceVideo = r"C:\Users\eray\Desktop\裝備影機影片\video_current_cut\not_cut_frame"
saveFolder = r"C:\Users\eray\Desktop\AI-VISION_ppe-collect\current_cut"
intervalCut = []#如果是空的 會整部都切，如果有值會只切指定frame範圍4*60+30, 5*60+15


numSkipFrame = 3
wayName = 1   #命名規則  0 自訂,  其他值 就看當下時間
isShowIm = True
thresh = 40.0   #比這個值低的才會切出來   #40

def imBaseName(videoName):    #檔名的命名規則
    
    baseWord = videoName.partition("_")[2]
    baseWord = baseWord.rpartition("_")[0]
    
    return baseWord
    
def imBaseName2(videoName):    #檔名的命名規則
    
    resultStr = ""
    baseWord = videoName.partition(" ")[2]
    baseWord1, _, baseWord2 = baseWord.partition("_")
    baseWord2 = baseWord2.rpartition("_")[0]
    
    for i in baseWord1.split("-"):
        resultStr += i
        
    resultStr += "_"
    
    for i in baseWord2.split("_"):
        resultStr += i
    
    return resultStr

def imBaseName3(videoName):    #檔名的命名規則
    
    if videoName.find(".") != -1:
        resultStr = videoName.rpartition(".")[0]
    else:
        resultStr = videoName
        
    return resultStr

def filterFrame(frameBase, frameNow, thresh):
    
    valueRSNR = psnr(frameBase, frameNow)
    print("valueRSNR:", valueRSNR)
    if thresh > valueRSNR:
        return True
    
    return False

def psnr(img1, img2):
   mse = np.mean((img1 - img2) ** 2 )
   if mse < 1.0e-10:
      return 100
   return 10 * math.log10(255.0**2/mse)
    
def createFolder(targetPath):
    if not os.path.exists(targetPath):
        os.makedirs(targetPath)


if __name__ == '__main__':

    listVideo = []
    listVideo += glob.glob(os.path.join(sourceVideo, "*.3gp"))
    listVideo += glob.glob(os.path.join(sourceVideo, "*.mkv"))
    listVideo += glob.glob(os.path.join(sourceVideo, "*.avi"))
    listVideo += glob.glob(os.path.join(sourceVideo, "*.mp4"))
    listVideo += glob.glob(os.path.join(sourceVideo, "*.MP4"))
    listVideo += glob.glob(os.path.join(sourceVideo, "*.MOV"))

    listVideo.sort()
    print(listVideo)
   
    if isShowIm:
        cv2.namedWindow('base', 0)
        cv2.namedWindow('now', 0)
   
    '''
    for i in range(0, len(intervalCut)):
        baseName = os.path.basename(listVideo[0])[:-4]
        if wayName == 0:  
            baseName = imBaseName2(baseName)
        else:
            baseName = time.strftime('%Y%m%d_%H%M%S')
        
        cap = cv2.VideoCapture(listVideo[0])
        startFrameNum = intervalCut[i][0]*cap.get(cv2.CAP_PROP_FPS)
        endFrameNum = intervalCut[i][1]*cap.get(cv2.CAP_PROP_FPS)
        cap.set(cv2.CAP_PROP_POS_FRAMES, startFrameNum)
        
        baseName_count = 0    
        
        frameTotal = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if frameTotal < 1:
            frameTotal = 3600*30
        d = int(math.log10(frameTotal)) +1
        counter = int(math.pow(10, d))
        
        frameBase = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), np.uint8)
        frameBase.fill(255)
        
        ret, frameNow = cap.read()
        
        createFolder( os.path.join(saveFolder, str(i)) )
        
        while ret and (baseName_count - counter) < endFrameNum:
        
            baseName_count = counter + int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            
            if filterFrame(frameBase, frameNow, thresh):
                print(str(counter+baseName_count)[1:])
                #print( os.path.join(saveFolder, str(i), baseName + '_' +str(counter+baseName_count)[1:]+'.jpg') )
                cv2.imwrite(os.path.join(saveFolder, str(i), baseName + '_' +str(counter+baseName_count)[1:]+'.jpg'), frameNow)
                frameBase = frameNow.copy()
            
            else:
                print ("skip: {0}\t".format(str(baseName_count)[1:]), end="\r")
                
            if isShowIm:
                cv2.imshow('base', frameBase)
                cv2.imshow('now', frameNow)
                cv2.waitKey(1)
            
            #略過畫面用
            for j in range(0, numSkipFrame):
                ret, frameNow = cap.read()
            #time.sleep(3)
        
    '''
   
    for i in range(len(listVideo)):
        #counter = 100001
        baseName = os.path.basename(listVideo[i])[:-4]
        #print(baseName)
        if wayName == 1:  
            baseName = imBaseName(baseName)
            #print(baseName)
        else:
            baseName = time.strftime('%Y%m%d_%H%M%S')
        
        cap = cv2.VideoCapture(listVideo[i])
        if len(intervalCut) > 1:
            cap.set(cv2.CAP_PROP_POS_FRAMES, intervalCut[0]*cap.get(cv2.CAP_PROP_FPS))
            endFrameNum = intervalCut[1]*cap.get(cv2.CAP_PROP_FPS)
        else:
            endFrameNum = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print(endFrameNum)    
        baseName_count = 0    
        
        frameTotal = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if frameTotal < 1:
            frameTotal = 3600*30
        d = int(math.log10(frameTotal)) +1
        counter = int(math.pow(10, d))
        
        frameBase = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), np.uint8)
        frameBase.fill(255)
        
        ret, frameNow = cap.read()
        #print (listVideo[i])
        
        print(os.path.join(saveFolder, baseName))																																											
        createFolder(os.path.join(saveFolder, baseName))
        
        #while ret and (baseName_count - counter) < endFrameNum:
        while (baseName_count - counter) < endFrameNum:
            baseName_count = counter + int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            
            #frame = np.rot90(frame)
            if filterFrame(frameBase, frameNow, thresh):
                print( os.path.join(os.path.join(saveFolder, baseName), baseName + '_' +str(counter+baseName_count)[1:]+'.jpg') )
                cv2.imwrite(os.path.join(os.path.join(saveFolder, baseName), baseName + '_' +str(counter+baseName_count)[1:]+'.jpg'), frameNow)
                frameBase = frameNow.copy()
            #counter += 1
            else:
                print ("skip: {0}\t".format(str(baseName_count)[1:]), end="\r")
                
            if isShowIm:
                cv2.imshow('base', frameBase)
                cv2.imshow('now', frameNow)
                cv2.waitKey(1)
            
            #略過畫面用
            for i in range(0, numSkipFrame):
                ret, frameNow = cap.read()
                
            while ret==False and (baseName_count - counter) < endFrameNum:
                ret, frameNow = cap.read()
                baseName_count += 1
            #time.sleep(3)

            
        
    
    
