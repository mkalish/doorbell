#!/usr/bin/python

import cv2

HAAR_CASCADE_PATH = "haarcascade_frontalface_alt.xml"

CAMERA_INDEX = 0

def detect_faces(image):
	faces = []
	detected = cascade.detectMultiScale(image, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (15,15))

	if len(detected) != 0:
		for x1, y1, x2, y2 in detected:
			faces.append((x1,y1,x2,y2))
	
	return faces


if __name__ == "__main__":
	cv2.namedWindow("Video", cv2.cv.CV_WINDOW_AUTOSIZE)

	capture = cv2.VideoCapture(CAMERA_INDEX)

	cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)

	faces = []

	i=0
	while True:
		image = capture.read()[1]

		if i%5==0:
			faces = detect_faces(image)

		for x1, y1, x2, y2 in faces:
			cv2.rectangle(image, (x1,y1), (x1+x2, y1+y2), (127,255,0), 2)
			sub_face = image[y1:y1+y2, x1:x1+x2]
			cv2.imwrite('data/images/lara/lara'+str(i)+'.pgm',sub_face)		


		cv2.imshow("Video", image)
		i += 1
		k = cv2.waitKey(33)
		
		if k == 27:
			cv2.destroyWindow("Video")
			break
