# Taller 1 – ROS2 TurtleBot2 (Grupo 5)

## Descripción
Implementación del Taller 1 del curso de Robótica utilizando ROS2 Humble y CoppeliaSim.
El proyecto incluye:

1. Control del TurtleBot2 por teclado (teleop).
2. Interfaz gráfica para visualización de la trayectoria.
3. Grabación del recorrido del robot en un archivo `.txt`.
4. Reproducción de trayectorias mediante un servicio ROS2.

## Requisitos
- Ubuntu 22.04
- ROS2 Humble
- CoppeliaSim (con plugin ROS2 correcto)
- Python 3

## Estructura
ros2_ws/
└── src/
├── turtle_bot_5
└── turtle_bot_5_interfaces


## Compilación
```bash
cd ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash


##Ejecucion
#Teleop
ros2 run turtle_bot_5 turtle_bot_teleop

#Player(Servicio)
ros2 run turtle_bot_5 turtle_bot_player

#Servicio
/turtle_bot_5/play_path


##Autores
Grupo 5

