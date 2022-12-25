#!/usr/bin/env python

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
marker_size  = 10
# Import the custom message type

# Create publishers for the marker center and ID
aruco_info_publisher = rospy.Publisher("/aruco/info", aruco_info, queue_size=1)

calib_path  = ""

camera_matrix = np.array([[698.30269162,   0,         482.23369024],
 [  0,         699.30531713, 281.24277949],
 [  0,           0,           1.        ]])
camera_distortion = np.array([[-0.14822482,  0.52992297, -0.005417,   -0.00265437, -0.75054646]])


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




