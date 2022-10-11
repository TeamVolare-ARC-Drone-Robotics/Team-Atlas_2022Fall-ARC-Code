from djitellopy import Tello
import cv2
import math
import time

drone = Tello()

drone.connect()
drone.takeoff()
time.sleep(1)

drone.streamon()

cv2.namedWindow("drone")
drone_stream = drone.get_frame_read()

#Import the face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
	#Read the incoming frames
	stream = drone_stream.frame
	#convert th frames to a grayscale image
	grayscale = cv2.cvtColor(stream, cv2.COLOR_BGR2GRAY)
	#process the image with comparision the face cascade and detect the face
	faces = face_cascade.detectMultiScale(grayscale, 1.1, 4)
	#If there is a face then
	for (x, y, w, h) in faces:
		cv2.rectangle(stream, (x, y), (x + w, y + h), (255, 0, 0), 2)
	cv2.imshow('Tello Footage', stream)

	key = cv2.waitKey(1) & 0xff
	if key == ord('q'):
		drone.land()
		drone_stream.stop()
		drone.streamoff()
		exit(0)
	elif key == ord('w'):
		drone.move_up(30)
	elif key == ord('s'):
		drone.move_down(30)
	elif key == ord('a'):
		drone.rotate_counter_clockwise(20)
	elif key == ord('d'):
		drone.rotate_clockwise(20)