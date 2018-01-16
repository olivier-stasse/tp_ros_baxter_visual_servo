import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

import baxter_insaros.utils as utils

def planif_baxter(pos_x,pos_y,pos_z,or_x, or_y, or_z, or_w, limb) :
    my_argv=['joint_states:=/robot/joint_states']
    moveit_commander.roscpp_initialize(my_argv)
    rospy.init_node('move_group_python_interface_tutorial',
                anonymous=True)

    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    if (limb =="left") :
        group = moveit_commander.MoveGroupCommander("left_arm")
    else :
        group = moveit_commander.MoveGroupCommander("right_arm")
    
    display_trajectory_publisher = rospy.Publisher(
                                    '/move_group/display_planned_path',
                                    moveit_msgs.msg.DisplayTrajectory)
    
    print "============ Waiting for RVIZ..."
    #rospy.sleep(10)
    print "============ Starting dancing "

    print "============ Reference frame: %s" % group.get_planning_frame()
    print "============ Reference frame: %s" % group.get_end_effector_link()
    print "============ Robot Groups:"
    print robot.get_group_names()

    print "============ Printing robot state"
    print robot.get_current_state()
    print "============"

    print "============ Generating plan "
    pose_target = geometry_msgs.msg.Pose()
    pose_target.position.x = pos_x
    pose_target.position.y = pos_y
    pose_target.position.z = pos_z

    pose_target.orientation.x = or_x
    pose_target.orientation.y = or_y
    pose_target.orientation.z = or_z
    pose_target.orientation.w = or_w 
    group.set_planner_id("RRTConnectkConfigDefault");

    # IK Solve request
    if (limb == "left"):
        joint_solution = utils.limb_ik_request('left', utils.make_poses(leftpose=pose_target))
    else :
       joint_solution = utils.limb_ik_request('right', utils.make_poses(rightpose=pose_target))
    
    print joint_solution 

    # Joint-space planing request
    group.set_joint_value_target(joint_solution)
    plan2 = group.plan()
    print plan2

    group.go(wait=True)

print '===== Debut exec'
i = 2
while (i > 0):
    planif_baxter( 0.96,0.14,-0.09,0.06,0.92,-0.02,0.3, 'left')
    planif_baxter( 0.98,0.0,-0.08,0.88,0.23,0.37,-0.11, 'right')

    planif_baxter( 0.66,0.24,-0.10,0.30,0.89,-0.08,0.30, 'left')
    planif_baxter( 0.70,-0.14,-0.11,0.730,0.62,0.24,0.12, 'right')
    i = i-1
