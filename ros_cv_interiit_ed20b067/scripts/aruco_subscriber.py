#!/usr/bin/env python
import rospy
from ros_cv_interiit_ed20b067.msg import aruco_info

def callback(aruco_info_message):
    # Print the marker ID and center coordinates
    print("Marker ID:", aruco_info_message.id)
    print("Center coordinates:", aruco_info_message.center)

def main():
    rospy.init_node('subscriber_node')
    sub = rospy.Subscriber('/aruco/info', aruco_info, callback)
    rospy.spin()

if __name__ == '__main__':
    main()
