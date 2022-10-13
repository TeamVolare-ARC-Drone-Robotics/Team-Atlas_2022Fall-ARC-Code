# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import sys
from djitellopy import Tello

#This array has the tag numbers stored in it
tagNums = []

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="DICT_ARUCO_ORIGINAL")
args = vars(ap.parse_args())
#Define the ArUCo tags
ARUCO_DICT = {
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
}

# load the ArUCo dictionary and grab the ArUCo parameters
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()

#create a instance of tello
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
	#Read the incoming streams
	stream = drone_stream.frame
	#convert th streams to a grayscale image
	grayscale = cv2.cvtColor(stream, cv2.COLOR_BGR2GRAY)
	# detect ArUco markers in the input stream
	(corners, ids, rejected) = cv2.aruco.detectMarkers(stream, arucoDict, parameters=arucoParams)
	# verify *at least* one ArUco marker was detected
	if len(corners) > 0:
		# flatten the ArUco IDs list
		ids = ids.flatten()

		# loop over the detected ArUCo corners
		for (markerCorner, markerID) in zip(corners, ids):
			tagNums.append(str(markerID))
			# extract the marker corners (which are always returned
			# in top-left, top-right, bottom-right, and bottom-left
			# order)
			corners = markerCorner.reshape((4, 2))
			(topLeft, topRight, bottomRight, bottomLeft) = corners

			# convert each of the (x, y)-coordinate pairs to integers
			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))

			# draw the bounding box of the ArUCo detection
			cv2.line(stream, topLeft, topRight, (0, 255, 0), 2)
			cv2.line(stream, topRight, bottomRight, (0, 255, 0), 2)
			cv2.line(stream, bottomRight, bottomLeft, (0, 255, 0), 2)
			cv2.line(stream, bottomLeft, topLeft, (0, 255, 0), 2)

			# compute and draw the center (x, y)-coordinates of the
			# ArUco marker
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)
			cv2.circle(stream, (cX, cY), 4, (0, 0, 255), -1)

			# draw the ArUco marker ID on the stream
			cv2.putText(stream, str(markerID),
						(topLeft[0], topLeft[1] - 15),
						cv2.FONT_HERSHEY_SIMPLEX,
						0.5, (0, 255, 0), 2)
 	# show the output frame
	cv2.imshow("DJI Tello EDU", stream)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		tagNums = set(tagNums)
		#delete any 1023 or 0 from the set
		if('0' in tagNums):
			tagNums.remove('0')
		if('1023' in tagNums):
			tagNums.remove('1023')
		print(tagNums)
		drone.land()
		drone_stream.stop()
		drone.streamoff()
		exit(0)
		break
	elif key == ord('w'):
		drone.move_up(20)
	elif key == ord('s'):
		drone.move_down(20)
	elif key == ord('a'):
		drone.move_left(20)
	elif key == ord('d'):
		drone.move_right(20)
	elif key == ord('e'):
		drone.rotate_clockwise(20)
	elif key == ord('r'):
		drone.rotate_counter_clockwise(20)

# do a bit of cleanup
cv2.destroyAllWindows()