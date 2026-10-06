#!/usr/bin/env bash
set -eo pipefail

if [ ! -f /opt/ros/jazzy/setup.bash ]; then
  echo "ERROR: ROS 2 Jazzy no está instalado en /opt/ros/jazzy."
  exit 1
fi

source /opt/ros/jazzy/setup.bash

sudo apt update
sudo apt install -y \
  git \
  python3-colcon-common-extensions \
  python3-rosdep \
  python3-vcstool \
  ros-jazzy-xacro \
  ros-jazzy-rviz2 \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-joint-state-publisher \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-urdf \
  ros-jazzy-urdfdom \
  ros-jazzy-urdf-tutorial \
  ros-jazzy-rmw-cyclonedds-cpp \
  liburdfdom-tools

if [ ! -e /etc/ros/rosdep/sources.list.d/20-default.list ]; then
  sudo rosdep init || true
fi
rosdep update || true

WS="$HOME/grupo_03_doosan_m0609_ws"
if [ -e "$WS" ]; then
  echo "ERROR: ya existe $WS"
  echo "Para proteger el trabajo existente, el instalador no lo borrará."
  echo "Si esta es una instalación de prueba antigua y deseas empezar de cero, bórrala manualmente y vuelve a ejecutar instalar.sh."
  exit 1
fi
mkdir -p "$WS/src"
cd "$WS/src"
git clone --depth 1 --branch humble --filter=blob:none --sparse https://github.com/DoosanRobotics/doosan-robot2.git
cd doosan-robot2
git sparse-checkout set dsr_description2
cd "$WS/src"
PKG="$WS/src/grupo03_doosan_m0609_bringup"
mkdir -p "$PKG/launch" "$PKG/rviz"
cp /opt/ros/jazzy/share/urdf_tutorial/rviz/urdf.rviz "$PKG/rviz/display.rviz"
cat > "$PKG/package.xml" <<'EOF'
<?xml version="1.0"?>
<package format="3">
  <name>grupo03_doosan_m0609_bringup</name>
  <version>1.0.0</version>
  <description>Launch de visualización para la práctica IMT-342.</description>
  <maintainer email="imt342.robotica@example.com">IMT-342 Robótica</maintainer>
  <license>MIT</license>
  <buildtool_depend>ament_cmake</buildtool_depend>
  <exec_depend>dsr_description2</exec_depend>
  <exec_depend>robot_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher_gui</exec_depend>
  <exec_depend>rviz2</exec_depend>
  <exec_depend>xacro</exec_depend>
  <exec_depend>rmw_cyclonedds_cpp</exec_depend>
  <export><build_type>ament_cmake</build_type></export>
</package>
EOF
cat > "$PKG/CMakeLists.txt" <<'EOF'
cmake_minimum_required(VERSION 3.8)
project(grupo03_doosan_m0609_bringup)
find_package(ament_cmake REQUIRED)
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/rviz")
  install(DIRECTORY rviz DESTINATION share/${PROJECT_NAME})
endif()
ament_package()
EOF
cat > "$PKG/launch/display.launch.py" <<'PY'
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, TimerAction
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    model = PathJoinSubstitution([
        FindPackageShare("dsr_description2"),
        "urdf",
            "m0609.white.urdf"
    ])
    robot_description = ParameterValue(
        Command([
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            model,
        ]),
        value_type=str,
    )
    rviz_config = PathJoinSubstitution([
        FindPackageShare("grupo03_doosan_m0609_bringup"),
        "rviz",
        "display.rviz",
    ])

    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )
    gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen",
    )
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
    )

    return LaunchDescription([
        SetEnvironmentVariable("RMW_IMPLEMENTATION", "rmw_cyclonedds_cpp"),
        rsp,
        rviz,
        TimerAction(period=1.0, actions=[gui]),
    ])
PY

cd "$WS"
rosdep install --from-paths src --ignore-src -r -y --rosdistro jazzy || true
colcon build --symlink-install --packages-up-to grupo03_doosan_m0609_bringup

cat > "$WS/entorno.sh" <<'EOF'
#!/usr/bin/env bash
source /opt/ros/jazzy/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
if [ -f "$HOME/grupo_03_doosan_m0609_ws/install/setup.bash" ]; then
  source "$HOME/grupo_03_doosan_m0609_ws/install/setup.bash"
fi
EOF
chmod +x "$WS/entorno.sh"

source "$WS/entorno.sh"
ros2 pkg prefix grupo03_doosan_m0609_bringup >/dev/null

echo
echo "INSTALACIÓN COMPLETA - Doosan M0609"
echo "Workspace: $WS"
echo "Para abrir el robot:"
echo "  cd $WS"
echo "  source entorno.sh"
echo "  ros2 launch grupo03_doosan_m0609_bringup display.launch.py"
