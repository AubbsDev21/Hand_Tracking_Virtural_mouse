import numpy as np
import time
import logging

try:
    import HandTrackingModule as htm
    import cv2
    import mediapipe as mp
    import pyautogui
except:
    logging.error("Please pip install packages")

capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)
detector = htm.FindHands()

while True:
    _, frame = capture.read()
    hand_positions = detector.getPosition(frame, range(21))

    for pos in hand_positions:
        cv2.circle(frame, pos, 5, (255,0,0), cv2.FILLED)

    ##Checking to see if index finger is up
    if len(hand_positions) > 0:
        ## moving mouse mode
        if detector.index_finger_up(frame) == True and detector.middle_finger_up(frame) == False:
            print("index finger up")

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
