# import the necessary packages
import argparse
import time
import cv2
from djitellopy import Tello
drone = Tello()

# Initialize the arrays
targetTags = []

#TODO: INVERT THE 2ND ROW. The 2nd collumn should be inverted to allow for the drone to traverse the balloons in the 2nd level


# Initialize the arrays
targetTags = [2, 14, 6]

tagArray=[
     2, 9, 14, 18, 6, 11,
     9, 18, 2, 11, 6, 14,
     14, 11, 18, 9, 2, 6
]

popArray = [1 if i in targetTags else 0 for i in tagArray]

moveArray = [
    "", "", "", "", "", "",
    "", "", "", "", "", "",
    "", "", "", "", "", ""
]


def find_num_next_1(z):
    j = z
    c = 0
    x = 0
    if z == 17:
        return 0
    while x != 1:
        j += 1
        c += 1
        if popArray[j] or (j+1)/6 == 1 or (j+1)/6 == 2:
            x = 1
    return c


def decide_movements():
    global moveArray
    i = 0
    r = 0
    while i < 18:
        moveArray[i] = (
            ("P" if popArray[i] else "N")
            + ("R" if r == 0 or r == 2 else "L")
            + str(find_num_next_1(i))
        )
        # detect unnecessary instructions and remove them
        if i > 0:  # added because trying to access the array location before i=0 results in an index error
            if (moveArray[i][0] == "N")\
                    and ("D" not in moveArray[i-1]):
                    # Somehow, the code works without the thing below- but if it ain't broke, don't fix it!
                    # and (int(moveArray[i-1][2]) != int(moveArray[i][2])):
                moveArray[i] = ""
        if (i+1)/6 == 1 or (i+1)/6 == 2:
            moveArray[i] = (("P" if popArray[i] else "N") + "D1")
            r += 1
        if i == 17:
            moveArray[i] = (("P" if popArray[i] else "N") + "E0")
        i += 1

    #  Cleanup of empty strings
    moveArray = [i for i in moveArray if i]



def detect_tags():
    # This array has the tag numbers stored in it
    tagNums = []

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--type", type=str,
                    default="DICT_ARUCO_ORIGINAL",
                    help="DICT_ARUCO_ORIGINAL")
    args = vars(ap.parse_args())
    # Define the ArUCo tags
    ARUCO_DICT = {
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    }

    # load the ArUCo dictionary and grab the ArUCo parameters
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
    arucoParams = cv2.aruco.DetectorParameters_create()

    # create a instance of tello
    drone = Tello()

    drone.connect()
    drone.takeoff()
    time.sleep(1)

    drone.streamon()

    cv2.namedWindow("drone")
    drone_stream = drone.get_frame_read()

    while True:
        # Read the incoming streams
        stream = drone_stream.frame
        # convert th streams to a grayscale image
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
            # delete any 1023 or 0 from the set
            if '0' in tagNums:
                tagNums.remove('0')
            if '1023' in tagNums:
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
        elif key == ord('f'):
            drone.move_forward(30)
        elif key == ord('c'):
            drone.move_back(20)

    # do a bit of cleanup
    cv2.destroyAllWindows()


def decide_pops():
    for i in range(len(tagArray)):
        for j in range(len(tagArray[i])):
            if tagArray[i][j] in targetTags:
                popArray[i][j] = 1
    return popArray


def movedrone():
    for i in range(len(popArray)):
        for j in range(len(popArray[i])):
            if popArray[i][j] == 1:
                popBalloon()

            if i == 0 or i == 2:
                drone.move_right(20)
            elif i == 1:
                drone.move_left(20)

            if j == 6:
                drone.move_down(20)


def popBalloon():
    drone.move_forward(20)
    drone.move_back(20)

def goToFirstBallon():
    pass


#drone.connect()
#drone.streamon()
#drone.takeoff()

# decide_pops()
#goToFirstBallon()
#movedrone()

#drone.land()
print(popArray)
decide_movements()
print(moveArray)
