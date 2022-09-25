#Import Modules
from djitellopy import Tello
import cv2
drone = Tello()

#Connect before anything
drone.connect()
#Start Code
drone.takeoff()
drone.streamon()

#Go To the Ballons

drone.streamoff()
drone.land()
#End Code



