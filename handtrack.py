# -*- coding: utf-8 -*-

"""
Created on Tue Jul 18 17:21:51 2023

@author: Anay Panja
"""

import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils

ctime = 0
ptime = 0
while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB) 
    
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id ,lm in enumerate(handLms.landmark):
                print(id,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
    
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,55,0),3)
    
    
    cv2.imshow("image",img)
    
    cv2.waitKey(1)