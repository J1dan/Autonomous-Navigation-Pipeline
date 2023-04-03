#! /usr/bin/env python

import rospy
from move_base_virtual_wall_server.srv import CreateWall
from move_base_virtual_wall_server.srv import CreateWallRequest

rospy.wait_for_service('/virtual_wall_server/create_wall')
create_wall = rospy.ServiceProxy('/virtual_wall_server/create_wall', CreateWall)

req = CreateWallRequest()
req1 = CreateWallRequest()

req.id = 0
req.start_point.x = 1.2
req.start_point.y = 0.8
req.end_point.x = 2.7
req.end_point.y = 0.8


req1.id = 1
req1.start_point.x = 4.8
req1.start_point.y = 2
req1.end_point.x = 4.8
req1.end_point.y = 4

create_wall(req)
create_wall(req1)
