# Import Module
from djitellopy import Tello
import cv2
import GoTo_Ballons

drone = Tello()

# Connect before anything
drone.connect()
# Start Code
drone.takeoff()
drone.streamon()

# Go To the Ballons

# End Code
drone.streamoff()
drone.land()