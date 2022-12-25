#!/usr/bin/env python

import numpy as np
import cv2
import cv2.aruco as aruco
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import math
from geometry_msgs.msg import Point
from std_msgs.msg import Int32
import rosmsg
from ros_cv_interiit_ed20b067.msg import aruco_info
#--- Define Tag
id_to_find  = 72
marker_size  = 10 #- [cm]
# Import the custom message type

# Create publishers for the marker center and ID
aruco_info_publisher = rospy.Publisher("/aruco/info", aruco_info, queue_size=1)

def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6



def rotationMatrixToEulerAngles(R):
    assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])



calib_path  = ""

camera_matrix = np.array([[698.30269162,   0,         482.23369024],
 [  0,         699.30531713, 281.24277949],
 [  0,           0,           1.        ]])
camera_distortion = np.array([[-0.14822482,  0.52992297, -0.005417,   -0.00265437, -0.75054646]])

#--- 180 deg rotation matrix around the x axis
R_flip  = np.zeros((3,3), dtype=np.float32)
R_flip[0,0] = 1.0
R_flip[1,1] =-1.0
R_flip[2,2] =-1.0

#--- Define the aruco dictionary
aruco_dict  = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
parameters  = aruco.DetectorParameters_create()

# Initialize the ROS node and the CvBridge object
rospy.init_node("aruco_tracker")
bridge = CvBridge()

# Define a callback function to process the incoming video frames
def image_callback(image_message):
    try:
        # Convert the ROS image message to a NumPy array
        frame = bridge.imgmsg_to_cv2(image_message, "bgr8")
    except CvBridgeError as e:
        print(e)

    # Process the frame using the existing code
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters)
    if ids is not None and ids[0] == id_to_find:
        # Estimate the pose of the marker
        ret = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)
        info_msg = aruco_info()
        # Unpack the output, get only the first
        rvec, tvec = ret[0][0,0,:], ret[1][0,0,:]
        # Publish the center of the marker
        info_msg.center.x = tvec[0]
        info_msg.center.y = tvec[1]
        info_msg.center.z = tvec[2]
        info_msg.id = id_to_find
        aruco_info_publisher.publish(info_msg)
        # Draw the detected marker and put a reference frame over it
        aruco.drawDetectedMarkers(frame, corners)
        cv2.drawFrameAxes(frame, camera_matrix, camera_distortion, rvec, tvec, 10)

        
        # Obtain the rotation matrix tag->camera
        R_ct    = np.matrix(cv2.Rodrigues(rvec)[0])
        R_tc    = R_ct.T

        # Get the attitude in terms of euler 321 (Needs to be flipped first)
        pitch_marker, yaw_marker, roll_marker = rotationMatrixToEulerAngles(R_flip*R_tc)

        
    else:
        # Draw an empty picture
        aruco.drawDetectedMarkers(frame, corners)
    
    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
if __name__ == "__main__":
   
    rospy.init_node("aruco_tracker")
    bridge = CvBridge()

    image_sub = rospy.Subscriber("/image/aruco", Image, image_callback)

    rospy.spin()

