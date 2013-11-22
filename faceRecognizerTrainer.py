#!/usr/bin/python

import os
import numpy as np
import sys
import cv2
import logging
import shutil
from peewee import *


HAAR_CASCADE_PATH = "haarcascade_frontalface_alt.xml"

cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)

def detect(img, cascade):
	gray = to_grayscale(img)
	rects = cascade.detectMultiScale(gray, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (15,15))

	if len(rects) == 0:
		print 'did not find a face'
		return []
	return []

def detect_faces(img):
	faces = []
	gray = to_grayscale(img)
	detected = cascade.detectMultiScale(gray, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (15,15))
	if len(detected) != 0:
		print 'found faces'		
		for x1, y1, x2, y2 in detected:
			faces.append((x1, y1, x2, y2))

	return faces
	

def to_grayscale(img):
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	gray = cv2.equalizeHist(gray)
	return gray

def contains_face(img):
	return len(detect_faces(img)) > 0

def crop_faces(img, faces):
	for face in faces:
		x, y, w, h = [result for result in face]
		return img[y:y+h, x:x+w]



def load_images_to_db(path):
	for dirname, dirnames, filenames in os.walk(path):
		for subdirname in dirnames:
			subject_path = os.path.join(dirname, subdirname)
			label = Label.get_or_create(name=subdirname)
			label.save()
			for filename in os.listdir(subject_path):
				path = os.path.abspath(os.path.join(subject_path, filename))
				logging.info('saving path %s'  % path)
				image = Image.get_or_create(path=path, label=label)
				image.save()

def load_images_from_db():
	images, labels = [],[]
	for label in Label.select():
		for image in label.image_set:
			try:
				print image.path
				cv_image = cv2.imread(image.path, cv2.IMREAD_GRAYSCALE)
				cv_image = cv2.resize(cv_image, (100,100))				
				images.append(cv_image)
				labels.append(label.id)
			except IOError, (errno, strerror):
				print "IOError({0:}): {1}".format(errno, strerror)
	return images, np.asarray(labels)



def train():
	images, labels = load_images_from_db()
	model = cv2.createFisherFaceRecognizer()
	model.train(images, labels)
	model.save("model.mdl")

def predict(cv_image):
	faces = detect_faces(cv_image)
	result = None
	if len(faces) > 0:
		print 'found a face attempting to predict'
		cropped = to_grayscale(crop_faces(cv_image, faces))
		resized = cv2.resize(cropped, (100,100))

		model = cv2.createFisherFaceRecognizer()
		model.load("model.mdl")

		prediction = model.predict(resized)
		result = {
			'face': Label.get(Label.id == prediction[0]).name,
			'distance': prediction[1]
		}

	return result


db = SqliteDatabase("data/images.db")
class BaseModel(Model):
	class Meta:
		database = db


class Label(BaseModel):
	IMAGE_DIR = "data/images"
	name = CharField()

	def persist(self):
		path = os.path.join(self.IMAGE_DIR, self.name)

		if(os.path.exists(path)) and len(os.listdir(path)) >= 10:
			shutil.rmtree(path)

		if not os.path.exists(path):
			logging.info("Created directory: %s" % self.name)
			os.makedirs(path)

		Label.get_or_create(name=self.name)

		self.save()

class Image(BaseModel):
	IMAGE_DIR = "data/images"

	path = CharField()
	
	label = ForeignKeyField(Label)

	def persist(self, cv_image):
		path = os.path.join(self.IMAGE_DIR, self.label.name)
		nr_of_images = len(os.listdir(path))
		if nr_of_images >= 10:
			return 'Done'
		faces = detectFaces(cv_image)
		if(len(faces)) > 0:
			path += "/%s.jpg" % nr_of_images
			path = os.path.abspath(path)
			logging.info("Saving %s" % path)
			cropped = to_grayscale(crop_faces(cv_image, faces))
			cv2.imwrite(path, cropped)
			self.path = path
			self.save()




if __name__ == "__main__":
	#train()
	#load_images_to_db("data/images")



	cv2.namedWindow("Video", cv2.cv.CV_WINDOW_AUTOSIZE)

	#cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)

	capture = cv2.VideoCapture(0)	

	i = 0
	badPredictions = 0
	while True:
		image = capture.read()[1]

				
		if i%5 == 0:
			if badPredictions < 10:
				result = predict(image)
				if result:
					#print 'face: '+ str(result['face']) 
					#print 'distance: ' + str(result['distance'])
					if result['distance'] > 1300:
						badPredictions += 1
					else:
						print 'hello '+ result['face']
			else:
				#name = raw_input("Enter your name: ")
				#label = Label.get_or_create(name=name).persist()
				#image = Image(label=label).persist(image)
				print 'adding to database' + name
			faces = detect_faces(image)
			for x1, y1, x2, y2 in faces:
				cv2.rectangle(image, (x1, y1), (x1+x2, y1+y2), (127, 255, 0), 2)		
				croppedFace = image[y1:y1+y2, x1:x1+x2]		
		cv2.imshow("Video", image)
		i += 1

		k = cv2.waitKey(33)
		if k == 27:
			cv2.destroyWindow("Video")
			break

