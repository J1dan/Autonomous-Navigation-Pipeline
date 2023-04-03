import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
import message_filters

class InitialPosePublisher:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('initial_pose_publisher')

        # Set up subscribers to robot's odometry topic
        self.odom_sub = message_filters.Subscriber('/odometry/filtered', Odometry)
        self.odom_time_sync = message_filters.TimeSynchronizer([self.odom_sub], queue_size=1)
        self.odom_time_sync.registerCallback(self.odom_callback)

        # Set up publisher to the initial pose topic
        self.initial_pose_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=1)

        # Set linear and angular velocity thresholds
        self.linear_vel_threshold = 0.02 # m/s
        self.angular_vel_threshold = 0.03 # rad/s

        self.pose_msg = None
        self.FLAG = False
        self.i = 0

        # Set up timer to publish initial pose every 3 seconds
        self.timer = rospy.Timer(rospy.Duration(3.0), self.publish_initial_pose)

    def odom_callback(self, odom_msg):
        # self.i+=1
        # if self.i != 5:
        #     return
        # else:
        #     self.i = 0
        # Check if robot is stationary
        linear_vel = odom_msg.twist.twist.linear.x
        angular_vel = odom_msg.twist.twist.angular.z

        if not self.FLAG: # Only update when the robot is moving
            print("Robot moving")
            self.pose_msg = odom_msg

        if abs(linear_vel) < self.linear_vel_threshold and abs(angular_vel) < self.angular_vel_threshold:
            self.FLAG = True
        else:
            self.FLAG = False

    def publish_initial_pose(self, event):
        if self.FLAG: # Only publish initial pose when the robot is stationary
            rospy.loginfo(f"Publishing initial pose")
            initial_pose_msg = PoseWithCovarianceStamped()
            initial_pose_msg.header.stamp = rospy.Time.now()
            initial_pose_msg.header.frame_id = 'map'
            initial_pose_msg.pose.pose = self.pose_msg.pose.pose
            self.initial_pose_pub.publish(initial_pose_msg)

if __name__ == '__main__':
    try:
        node = InitialPosePublisher()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
