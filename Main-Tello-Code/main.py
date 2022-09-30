# Import Module
from djitellopy import Tello
import cv2

drone = Tello()

#Start Writing Functions
def popBallons():
    drone.move_forward(20)


# Connect before anything
drone.connect()
# Start Code
drone.takeoff()
drone.streamon()

# Go To the Ballons

# End Code
drone.streamoff()
drone.land()