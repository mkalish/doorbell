#!/usr/bin/python

import cv2
from faceDetect import detectFace, box


cv2.namedWindow("camera", 1)


camera_port = 0

ramp_frames = 30

camera = cv2.VideoCapture(camera_port)

while True:
	img = camera.read()[1]
	rects, img = detectFace(img)
	box(rects, img)
	cv2.imshow("camera", img)
	if cv2.waitKey(0) : break
cv2.destroyWindow("camera")




