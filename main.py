from djitellopy import Tello
import cv2
drone = Tello()

#Start Code
drone.takeoff()
drone.streamon()

drone.flip_forward()

drone.streamoff()
drone.land()