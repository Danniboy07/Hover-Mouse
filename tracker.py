import cv2
import mediapipe as mp
import pyautogui

screen_w, screen_h = pyautogui.size()
cam = cv2.VideoCapture(0)
pyautogui.FAILSAFE = False
hand = mp.solutions.hands.Hands()
old_x, old_y = 0, 0

def displacement(x, x1, y, y1):
    dis = round(((x1-x)**2 + (y1-y)**2)**0.5)
    xcord = x/x1*screen_w
    ycord = y/y1*screen_h
    


while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand.process(rgb_frame)
    landmarks = output.multi_hand_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmarks:
        landmark = landmarks[0].landmark
        points = [landmark[8]]
        for id, mark in enumerate(points):
            x = int(mark.x*screen_w)
            y = int(mark.y*screen_h)
            cv2.circle(frame, (int(mark.x*frame_w), int(mark.y*frame_h)), 3, (0, 255, 0))
            print(abs(x - old_x) + abs(y - old_y))
            if abs(x - old_x) + abs(y - old_y) > 20:
                pyautogui.moveTo(x*1.5-screen_w/4, y*1.5-screen_h/4)
            old_x, old_y = x, y

            

    cv2.imshow('Hover Mouse!', frame)
    cv2.waitKey(1)