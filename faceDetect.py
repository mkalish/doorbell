#!/usr/bin/python

import cv2
import cv2.cv as cv


def detectFace(path):
	img = path
	#img_gray = cv2.cvtColor(img, cv.CV_RGB2GRAY)
	#img_gray = cv2.equalizeHist(img_gray)
	cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
	rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (15,15))

	if len(rects) == 0:
		return [], img
	rects[:, 2:] += rects[:, :2]
	return rects, img

def box(rects, img):
	for x1, y1, x2, y2 in rects:
		cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
	cv2.imwrite('detected.jpg', img)

#rects, img = detectFace("test.jpg")
#box(rects, img)
