from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Define the path to the URDF file
    vehicle_urdf_path = FindPackageShare('vehicle').find('vehicle') + '/urdf/B4WTYPE3.urdf'
    
    return LaunchDescription([
        # Include Gazebo empty world launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [FindPackageShare('gazebo_ros').find('gazebo_ros'), '/launch/gazebo.launch.py']
            ),
        ),

        # Static Transform Publisher Node
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='tf_footprint_base',
            arguments=['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', 'base_link', 'base_footprint']
        ),

        # Spawn Model Node
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_model',
            arguments=[
                '-file', vehicle_urdf_path,
                '-entity', 'vehicle'
            ],
            output='screen'
        ),
    ]) 

