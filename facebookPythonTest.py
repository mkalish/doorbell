#!/usr/bin/python

import os
import shutil
import facebook
import urllib
import cv2
import Image
import faceRecognizerTrainer
from urlparse import urlparse, parse_qs

access_token = 'CAACrZAWorZACkBAJvtCHzJhBlmZCILGeuP1K7i7pUUBKhsgYzOHowNaujFasnoOcKGOvx3wmO6BPnEqs8UHZA3qa1fdBP2v6htuZCt0kk8k85XiEtz1V79KN0kbHHSrspMgjYmMXZCwTCg12TVWvfdzO5FdGXZCpZBwCuXVUxtK9AHZBhWBXh85zbF2KdmXpZBzboZD'


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


def get_photos_and_tags(until=None, limit=None):

	graph = facebook.GraphAPI(access_token)
	args={'fields':'tags.fields(name,x,y),source, height, width'}
	
	if until and limit:
		#print until
		#print limit
		args['limit'] = str(limit)
		args['until'] = str(until)	
	print args
	photos_and_tags = graph.request(
		path = "/me/photos",
		args=args
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

def process_facebook_data(photos_and_tags):
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
                                                        clean_name = "".join(name.split())
                                                        path = "data/friends/"+clean_name
                                                        if not os.path.exists(path):
                                                                print 'adding directory'
                                                                os.mkdir(path)
                                                        nr_of_pics = len(os.listdir(path))
                                                        x1, y1, x2, y2 = face
                                                        cropped_face = faceRecognizerTrainer.to_grayscale(image[y1:y1+y2, x1:x1+x2])
                                                        cv2.imwrite(path+"/pic_"+str(nr_of_pics)+".pgm", cropped_face)


if __name__ == "__main__":
	

	results = get_photos_and_tags()
	photos_and_tags = results['data']
	next_page = results['paging']['next']

	while True:
		process_facebook_data(photos_and_tags)
		
		fields = parse_qs(urlparse(next_page).query, '&')
		until = fields['until'][0]
		limit = fields['limit'][0]
		
		results = get_photos_and_tags(until, limit)

		if not results['paging']['next']:
			process_facebook_data(results['data'])
			print 'done'
			break
		else:
			process_facebook_data(results['data'])
			next_page = results['paging']['next']
			




