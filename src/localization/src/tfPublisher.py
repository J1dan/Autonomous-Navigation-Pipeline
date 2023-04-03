import rospy
import tf2_ros
from geometry_msgs.msg import TransformStamped

rospy.init_node('tf_publisher')

tf_broadcaster = tf2_ros.TransformBroadcaster()

transform = TransformStamped()

transform.header.frame_id = '/odom'
transform.child_frame_id = '/base_link'

transform.transform.translation.x = 0.486
transform.transform.translation.y = 0.107
transform.transform.translation.z = -0.000

transform.transform.rotation.x = 0.000
transform.transform.rotation.y = 0.000
transform.transform.rotation.z = 0.192
transform.transform.rotation.w = 0.981

transform.header.stamp = rospy.Time.now()

tf_broadcaster.sendTransform(transform)
rospy.spin()