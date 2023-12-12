import rclpy
from rclpy.node import Node
from rclpy.time import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Header
import time

class JointTrajectoryPublisher(Node):
    
    def __init__(self):

        super().__init__('joint_trajectory_publisher')
        self.publisher = self.create_publisher(JointTrajectory, '/scara_cpe_group_controller/joint_trajectory', 10)

        self.joint_trajectory = JointTrajectory()
        self.joint_trajectory.header = Header(frame_id='base_link')
        self.joint_trajectory.joint_names = ['shoulder_1_joint', 'shoulder_2_joint']

        self.point = JointTrajectoryPoint()

        #self.point.time_from_start = Duration(seconds=5.0).to_msg

    def publish_goal_trajectory(self):


        self.point.positions = [0.8, 0.6]
        self.joint_trajectory.points.append(self.point)

        self.publisher.publish(self.joint_trajectory)
        self.get_logger().info('Goal trajectory published')


    def publish_initial_trajectory(self):


        self.point.positions = [-0.5, -1.0]
        self.joint_trajectory.points.append(self.point)

        self.publisher.publish(self.joint_trajectory)
        self.get_logger().info('Initial trajectory published')

def main(args=None):

    rclpy.init(args=args)

    joint_trajectory_publisher = JointTrajectoryPublisher()

    try:
        while rclpy.ok():

            joint_trajectory_publisher.publish_goal_trajectory()
            time.sleep(3.0)
            joint_trajectory_publisher.publish_initial_trajectory()
            time.sleep(3.0)

    except KeyboardInterrupt:
        pass

    joint_trajectory_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
