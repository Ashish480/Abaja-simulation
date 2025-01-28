cmake_minimum_required(VERSION 3.8)
project(vehicle)

# Set compile options for warnings
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(ackermann_msgs REQUIRED)
find_package(rclpy REQUIRED)         # Add rclpy for Python nodes
find_package(rclcpp REQUIRED)
find_package(gazebo_dev REQUIRED)    # Gazebo Classic development files
find_package(gazebo_msgs REQUIRED)   # Gazebo Classic messages
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tf2 REQUIRED)

# Add executable
add_executable(acker src/ackermann_control.cpp)

# Link Gazebo Classic libraries to the target
target_link_libraries(acker
  ${GAZEBO_LIBRARIES}
)

# Add dependencies to the target
ament_target_dependencies(acker 
  rclcpp
  ackermann_msgs
  gazebo_dev
  gazebo_msgs
)

# Specify include directories (for Gazebo headers)
target_include_directories(acker PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${GAZEBO_INCLUDE_DIRS}
)

# Add Python nodes (scripts)
install(
  PROGRAMS scripts/calibration_publisher.py
  DESTINATION lib/${PROJECT_NAME}/scripts
)

# Install mesh files
install(
  DIRECTORY meshes
  DESTINATION share/${PROJECT_NAME}/
)

# Install URDF files
install(
  DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}/
)

# Install configuration files (if required)
install(
  DIRECTORY config
  DESTINATION share/${PROJECT_NAME}/
)

# Install executables
install(TARGETS
  acker
  DESTINATION lib/${PROJECT_NAME})

# Enable testing if specified
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  
  # Skip specific linters if no copyright/license (can be removed once added)
  set(ament_cmake_cpplint_FOUND TRUE)
  set(ament_cmake_copyright_FOUND TRUE)

  ament_lint_auto_find_test_dependencies()
endif()

# Declare the package
ament_package()

