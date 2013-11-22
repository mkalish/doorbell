#!/usr/bin/python

import cv2


HAAR_CASCADE_PATH = "haarcascade_frontalface_alt.xml"



def diffImg(t0, t1, t2):
	d1 = cv2.absdiff(t2, t1)
	d2 = cv2.absdiff(t1, t0)
	return cv2.bitwise_and(d1, d2)

def detectFaces(image):
	#print 'Detecting faces'
	cv2.imshow("Captured Movement", image)
	faces = []
	detected = cascade.detectMultiScale(image, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (15,15))
	

	if len(detected) != 0:
		print 'found a face'
		for x1, y1, x2, y2 in detected:
			faces.append((x1,y1,x2,y2))	

	return faces

def cropFace(image, faces):
	global NUMBER_OF_FACES

	croppedFaces = []
	for x1, y1, x2, y2 in faces:
		face = image[y1:y1+y2, x1:x1+x2]
		NUMBER_OF_FACES += 1
		cv2.imwrite('capturedFace_' + str(NUMBER_OF_FACES) +'.jpg', face)


if __name__ == "__main__":
	
	
	cv2.namedWindow("Captured Movement", cv2.cv.CV_WINDOW_AUTOSIZE)
	
	cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)

	NUMBER_OF_FACES = 0

	capture = cv2.VideoCapture(0)
	#set the frame rate
	#capture.set(6, 20)
		
	t_minus = capture.read()[1]
	t = capture.read()[1]
	t_plus = capture.read()[1]

	i=0
	while True:
		if i%2 == 0:
			dif = diffImg(cv2.cvtColor(t_minus, cv2.COLOR_RGB2GRAY), cv2.cvtColor(t, cv2.COLOR_RGB2GRAY), cv2.cvtColor(t_plus, cv2.COLOR_RGB2GRAY))
			totalDifference  = cv2.countNonZero(dif)
			
			if totalDifference > 150000:
				
				
				faces = detectFaces(t)
				if len(faces) > 0:
					print 'face found'
					cropFace(t, faces)

					
					
			t_minus = t
			t = t_plus
			t_plus = capture.read()[1]
		i = i+1
		k = cv2.waitKey(33)
		if k == 27:
			break
