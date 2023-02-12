import os
import yaml
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import xacro


def load_file(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, "r") as file:
            return file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None

def generate_launch_description():
    robot_description_config = xacro.process_file(
        os.path.join(
            get_package_share_directory("cr3_1_config"),
            "config",
            "cr3_description.urdf.xacro",
        )
    )
    robot_description = {"robot_description": robot_description_config.toxml()}
    robot_description_semantic_config = load_file(
        "cr3_1_config", "config/cr3_description.srdf"
    )
    robot_description_semantic = {
        "robot_description_semantic": robot_description_semantic_config
    }

    rviz_base = os.path.join(get_package_share_directory("cr3_description"), "urdf")
    rviz_config = os.path.join(rviz_base, "moveit.rviz")
    rviz_node_tutorial = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config],
        parameters=[robot_description,
            robot_description_semantic,],
    )
    joint_state_publisher_gui = Node(
        name="joint_state_publisher_gui",
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        parameters=[robot_description],
    )
    # Publish TF
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )
    return LaunchDescription(
        [
            # tutorial_arg,
            # db_arg,
            # rviz_node,
            rviz_node_tutorial,
            robot_state_publisher,
            joint_state_publisher_gui,
        ]
    )
