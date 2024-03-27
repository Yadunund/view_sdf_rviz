cmake_minimum_required(VERSION 3.8)
project(view_sdf_rviz)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch models rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_environment_hooks("models.dsv.in")

ament_package()
