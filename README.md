# primer_parcial_grupo3
Repositorio del primer parcial del grupo 3 de robotica simulacion de cinematica directa e inversa del robot doosan_m0609.

## 1) Clonar el repositorio 
Al clonar el repositorio tendras la carpeta "grupo_03_doosan_m0609_ws" donde estaran todos los archivos necesarios.

## 2) Abrir Rviz2
Entra a la carpeta "grupo_03_doosan_m0609_ws" y ejecuta el comando ./abrir.sh donde se abrira el rviz con el robot y el joint_state_publisher. Para poder ejecutar los nodos de cinematica inversa y directa tienes que cerrar la ventana que se llama joint_state_publisher dado que este es un publicador y no se podra ejecutar el nodo.

## 3) Ejecutar nodo de cinematica directa
Posteriormente abre una nueva terminal y sin cerrar la que esta corriendo el rviz y vuelve a entrar a la carpeta "grupo_03_doosan_m0609_ws" y ejecuta estos comandos 

- source /opt/ros/jazzy/setup.bash
- colcon build
- source install/setup.bash

y ya podras correr el nodo de cinematica directa ejecutando el siguiente comando

- ros2 run grupo_03_doosan_m0609_tasks cinematica_directa_executable

despues te pedira que pongas angulos en grados para cada joint y te dara la posicion alcanzada en x, y, z, lo puedes verificar en rviz que el robot se movio y tambien puedes verificar las coordenadas en rviz, veras al costado una ventana que dice displays, en esa dice TF en TF dice link6 y en link6 podras ver la posicion
