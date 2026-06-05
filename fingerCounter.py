import cv2 as cv
import numpy as np
import time
import mediapipe as mp

class handDetector():
    def __init__(self, mode=False, max_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw=True):
        imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLm in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLm.landmark):
                    if draw:    
                        self.mpDraw.draw_landmarks(frame, handLm, self.mpHands.HAND_CONNECTIONS)

        return frame

    def findPosition(self, frame, handNum = 0, draw=True):
        lmlist = []
        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]

            for id, lm in enumerate(myHand.landmark):
                h,w,c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id,cx,cy])
                if draw:
                    cv.circle(frame, (cx,cy), 10, (255,0,255), cv.FILLED)

        return lmlist



    


def handSigns(fingers, frame, distance):
    if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:
        cv.putText(frame, 'peace', (10, 140), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 2)
    elif fingers[1] == 0 and fingers[2] == 0 and fingers[0] == 1 and fingers[3] == 0 and fingers[4] == 0:
        cv.putText(frame, 'thumbs up', (10, 140), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 2)
    elif fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 1 and fingers[3] == 0 and fingers[4] == 1:
        cv.putText(frame, 'lets rock', (10, 140), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 2)
    elif fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1 and fingers[3] == 1 and fingers[4] == 1:
        cv.putText(frame, 'hello', (10, 140), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 2)
    elif fingers[1] == 0 and fingers[2] == 1 and fingers[0] == 1 and fingers[3] == 1 and fingers[4] == 1 and distance <= 40:
        cv.putText(frame, 'perfect', (10, 140), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 2)
    return frame
def main():
    cTime = 0
    pTime = 0
    fps = 0
    detect = handDetector()
    capture = cv.VideoCapture(0)
    while True:
        fingers = []

        success, frame = capture.read()
        frame = detect.findHands(frame)

        lmlist = detect.findPosition(frame)
        if len(lmlist) != 0:
            for i in range(4, 21, 4):
                if i == 4:
                    if lmlist[i][1] >= lmlist[i-1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:
                    if lmlist[i][2] < lmlist[i-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

        
        print((fingers), sum(fingers))
        if len(fingers) != 0:
            distance = np.sqrt((pow(lmlist[8][1] - lmlist[4][1],2)) + (pow(lmlist[4][2] - lmlist[8][2],2)))
            frame = handSigns(fingers, frame, distance)
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv.putText(frame, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 2)
        cv.imshow('count', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break


main()