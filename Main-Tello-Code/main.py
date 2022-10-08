# Import Module
from djitellopy import Tello
import cv2
# import keyboard

drone = Tello()

# #Start Writing Functions
# def popBallons():
#     drone.move_forward(20)


# Connect before anything
drone.connect()


# Test Movement
# drone.flip_forward()

# Go To the Balloons
def droneInformation():
    print("Battery: ", drone.get_battery(),"%")
    print("Yaw: ", drone.get_yaw())
    print("Roll: ", drone.get_roll())
    print("Pitch: ", drone.get_pitch())
    print("Height: ", drone.get_height())
    print("Pressure: ", drone.get_barometer())
    print("Flight Time: ", drone.get_flight_time())

land = False
while land == True:

    print(droneInformation())

# This part might work for the steam
    drone.streamon()

    while True:
        img = me.get_frame_read().frame
        cv2.imshow("Image", img)
        cv2.waitKey(1)



    key = input("Key Board Input: ")
    if key == "land":  # ESC
        land = True
    elif key == 'w':
        drone.move_forward(30)
    elif key == 's':
        drone.move_back(30)
    elif key == 'a':
        drone.move_left(30)
    elif key == 'd':
        drone.move_right(30)
    elif key == 'e':
        drone.rotate_clockwise(30)
    elif key == 'q':
        drone.rotate_counter_clockwise(30)
    elif key == 'r':
        drone.move_up(30)
    elif key == 'f':
        # This section is to attempt to prevent the massive errors and stalls that happen when trying to
        # make the drone go down when it is close to the ground.
        try:
            drone.move_down(30)
        except:
            print("An error has been caught- perhaps the drone is too low to the ground?" +
                  f"\nIf so, make sure to use the 'land' command to get it to touch down.")


# End Code
drone.streamoff()
drone.land()