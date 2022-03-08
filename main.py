import numpy as np
import time
import logging

try:
    import HandTrackingModule as htm
    import cv2
    import mediapipe as mp
    import pyautogui
    import autopy
    pyautogui.FAILSAFE = False
    from hand_tracking import HandDetector
except:
    logging.error("Please pip install packages")

capture = cv2.VideoCapture(0)
frameH = capture.set(3, 640)
frameW = capture.set(4, 480)
frameR = 100
smoothening = 7
detector = htm.FindHands()
screenW, screenH = pyautogui.size()

plocX, plocY = 0, 0
clocX, clocY = 0, 0

while True:
    _, frame = capture.read()
    hand_positions = detector.getPosition(frame, range(21))
    print(hand_positions)

    x2, y2 = hand_positions[12][:1], hand_positions[12][1:]
    (x1, y1) = hand_positions[8]
    (x2, y2) = hand_positions[12]
    print(x1, y1, x2, y2)

    for pos in hand_positions:
        cv2.circle(frame, pos, 5, (255,0,0), cv2.FILLED)

    ##Checking to see if index finger is up
    if len(hand_positions) > 0:
        if detector.index_finger_up(frame) == True or detector.middle_finger_up(frame) == False:
            #convert values
            x3 = np.interp(x1, (0,frameW), (0, screenW))
                #np.interp(x1, (frameR, frameW - frameR), (0, frameW))
            y3 = np.interp(y1, (0, frameH), (0, screenH))
                ##np.interp(y1, (frameR, frameH - frameR), (0, frameH))
            x31 = int(x3)
            y31 = int(y3)
            # smoothen values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # Moving mouse
            pyautogui.move(x31, y31)
            ##cv2.circle(pyautogui.size(mouse), (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            ##plocX, plocY = clocX, clocY




            print("index finger up")


    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

