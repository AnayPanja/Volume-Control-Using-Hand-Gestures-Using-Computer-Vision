# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 11:33:03 2023

@author: Anay Panja
"""

import cv2
import time
import numpy as np
import hand_track_module as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wcam,hcam = 680,490

cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime = 0

detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
vol_range = volume.GetVolumeRange()

min_vol = vol_range[0]
max_vol = vol_range[1]

while True:
    success,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    
    if len(lmList) != 0:
        #print(lmList[2])
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        
        cv2.circle(img, (x1,y1), 15, (255,3,255),cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,3,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,3,255),2)
        
        length = math.hypot(x2-x1,y2-y1)
        
        vol = np.interp(length,[50,240],[min_vol,max_vol])
        volume.SetMasterVolumeLevel(vol, None)

        
        

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    
    cv2.putText(img, f'FPS:{int(fps)}', (40,70) , cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0),2)
    
    cv2.imshow("image",img)
    cv2.waitKey(1)
    