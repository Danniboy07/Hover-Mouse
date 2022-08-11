import cv2
import mediapipe as mp

cam = cv2.VideoCapture(0)

while True:
    _, frame = cam.read()
    cv2.imshow('Hover Mouse!', frame)
    cv2.waitKey(1)