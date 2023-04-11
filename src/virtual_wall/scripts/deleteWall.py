#! /usr/bin/env python

import rospy
from move_base_virtual_wall_server.srv import DeleteWall
from move_base_virtual_wall_server.srv import DeleteWallRequest

rospy.wait_for_service('/virtual_wall_server/delete_wall')
delete_wall = rospy.ServiceProxy('/virtual_wall_server/delete_wall', DeleteWall)

req = DeleteWallRequest()
req1 = DeleteWallRequest()

req.id = 0

req1.id = 1


delete_wall(req)
delete_wall(req1)
