#!/usr/bin/python

import os
import shutil
import facebook
import urllib
import cv2
import Image
import faceRecognizerTrainer



access_token = 'CAACrZAWorZACkBAEIBbZBuU955zoZCfyQCSDZCTsDzfyFjQvtEjQBfQLrhB5bjCnUXV7rw8ZB7YHg1ennV0XfTaQ4uZCve6uxKYbPtOqWNlO5bMvTXx5EQVcWZBK4naA1ncz9lDVRxfRQZBboaxj1HSYftUmr9iEzIFFkYrn2T9HMKULHjqsnRba3ZAD5f5ENtAVoZD'


def match_face_to_tag(face, tags):

	matched_faces = []	

	x1, y1, x2, y2 = face
	for name, coordinate in tags:
		tag_x, tag_y = coordinate
		x_distance = abs(x1-tag_x)
		y_distance = abs(y1-tag_y)
		if x_distance < 40 and y_distance < 40:
			matched_faces.append((face, name))

	return matched_faces


cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

temporary_data="data/temp"


def get_photos_and_tags():

	graph = facebook.GraphAPI(access_token)

	photos_and_tags = graph.request(
		path = "/me/photos",
		args={'fields':'tags.fields(name,x,y),source, height, width'}
	)

	return photos_and_tags	





def process_tags(tags, width, height):
	processedTags = []

	for tag in tags:
		xPercentage = tag['x']/100
		yPercentage = tag['y']/100
		actualX = int(width) * xPercentage
		actualY = int(height) * yPercentage
		processedTags.append((tag['name'], (actualX, actualY)))
	return processedTags



def process_image_for_faces(source):
	
	if not os.path.exists(temporary_data):
		os.mkdir(temporary_data)

	path = temporary_data+"/temp.jpg"
	urllib.urlretrieve(source, path)
	

	image = cv2.imread(path)

	faces = []
	
	detected = faceRecognizerTrainer.detect_faces(image)

	if len(detected) == 0:
		return faces
	else:
		return detected	


def clean_up():
	print 'Cleaning temp folder of pictures'
	#os.remove(temporary_data+"/*.jpg")	
	shutil.rmtree(temporary_data)


'''
path = "test.jpg"

urllib.urlretrieve(source, path)

image = cv2.imread(path)

faces = faceRecognizerTrainer.detect_faces(image)



if len(faces) == 0:
	print 'no faces found'
else:
	for face in faces:
		match_face_to_tag(face, processedTags)
	#print processedTags

'''

if __name__ == "__main__":
	photos_and_tags = get_photos_and_tags()['data']

		
	for photo in photos_and_tags:
		if 'tags' in photo:
			tags = photo['tags']
			source = photo['source']
			
			
			faces = process_image_for_faces(source)
			if len(faces) == 0:
				print 'No faces found continuing'
				clean_up()
				continue
			else:
				processedTags = process_tags(tags['data'], photo['width'], photo['height'])
				for face in faces:
					image = cv2.imread(temporary_data+"/temp.jpg")
					matched_faces = match_face_to_tag(face, processedTags)
					for face, name in matched_faces:
						if !os.dir.exists("/data/"+name):
							os.mkdir("/data/"+name):
			#print source
			#processedTags = process_tags(tags['data'], photo['width'], photo['height'])
			#print processedTags

