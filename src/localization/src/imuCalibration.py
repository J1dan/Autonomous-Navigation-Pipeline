#!/usr/bin/env python
import rospy
import time
import numpy as np
from sensor_msgs.msg import Imu

DEBUG = False
timeout = 10.0

class Server:
    def __init__(self):
        self.imu_yaw_vals_ = np.empty(0)
        self.imu_yaw_avg_ = 0
        self.recording = True

    def add_imu(self, z_val):
        if self.recording:
            if DEBUG: print("[INFO] yaw velocity got")
            self.imu_yaw_vals_ = np.append(self.imu_yaw_vals_, z_val)
        else:
            pass
       
    def time_cb(self):
        self.recording = False
        self.imu_yaw_avg_ = np.average(self.imu_yaw_vals_)
        if DEBUG: print("[INFO] Timeout Received")
        print("[INFO] Average yaw vel: " + str(self.imu_yaw_avg_))
        print("[INFO] Number of readings: " + str(len(self.imu_yaw_vals_)))


def imu_cb(msg):
    if server.recording == True:
        yaw = msg.angular_velocity.z
        server.add_imu(yaw)
    else:
        yaw_compensation = server.imu_yaw_avg_
        msg.angular_velocity.z = msg.angular_velocity.z - yaw_compensation
        imu_pub.publish(msg)
       

def timer_cb(msg):
    if DEBUG: print("[INFO] 5-second calibration timeout")
    server.time_cb()

if __name__ == "__main__":
    if DEBUG: print("[INFO] Imports done")
    print("[INFO] Sensor Calibration, do not move robot!!!")
    print("[INFO] Reading sensor inputs for " + str(timeout) + " seconds...")
    rospy.init_node("calibration")
    server = Server()
    imu_sub = rospy.Subscriber("/imu/data", Imu, imu_cb, queue_size=1)
    imu_pub = rospy.Publisher("/imu/data_calibrated", Imu, queue_size=1)
    timer = rospy.Timer(rospy.Duration(timeout), timer_cb, oneshot=True)
    rospy.spin()