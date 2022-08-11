import cv2
import mediapipe as mp
import pyautogui

screen_w, screen_h = pyautogui.size()
cam = cv2.VideoCapture(0)
pyautogui.FAILSAFE = False
hand = mp.solutions.hands.Hands()

def displacement(x, x1, y, y1):
    return round(((x1-x)**2 + (y1-y)**2)**0.5)
while True:
    old_x, old_y = 0, 0
    center = 0, 0
    max_width = None
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand.process(rgb_frame)
    landmarks = output.multi_hand_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmarks:
        landmark = landmarks[0].landmark
        points = [landmark[5], landmark[8]]
        for id, mark in enumerate(points):
            x = int(mark.x * screen_w)
            y = int(mark.y * screen_h)
            cv2.circle(frame, (int(mark.x*frame_w), int(mark.y*frame_h)), 3, (0, 255, 0))

            if abs(x-center[0]) <= 10 and not max_width:
                max_width = abs(y - center[1])
                print("Started tracking", max_width)
            if id == 1 and abs(old_x - x + old_y - y) >= 30 and max_width:
                #print(abs(old_x - x + old_y - y))
                print(x-center[0], y-center[1])
                print("this", displacement(x, center[0], y, center[1]))
                pyautogui.moveTo(round(screen_w*(x-center[0]/displacement(x, center[0], y, center[1]))), round(screen_h*(y-center[1]/displacement(x, center[0], y, center[1]))))
                old_x, old_y =  x, y
            elif id == 0:
                center = x, y

    cv2.imshow('Hover Mouse!', frame)
    cv2.waitKey(1)