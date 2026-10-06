# Primer_parcial_grupo3
Simulación de movimiento del robot doosan_m0609 mediante cinemática directa e inversa usando nodos en ros2. Hecho por:

Natalia Veizaga, Lucas Alvarez, Nicolas Gironda

Requerimientos minimos:

- Ubuntu 24.0
- ros2 jazzy

## 1) Clonar el repositorio 
Al clonar el repositorio tendras la carpeta "primer_parcial_grupo3". Dentro de esa carpeta se encuentran todos los archivos necesarios.

## 2) Instalar el entorno
Dentro de la carpeta "primer_parcial_grupo3" ejecuta el siguiente comando para dar permisos:

    sudo chmod 777 instalar.sh abrir.sh compilar.sh ejecutar_cd.sh ejecutar_ci.sh 

una vez hecho eso ejecuta el siguiente comando:

    ./instalar.sh

Este instalara lo necesario y creara una carpeta en el inicio de tu dispositivo llamada "grupo_03_doosan_m0609_ws". Solo es necesario realizar el proceso de instalacion una vez, en caso de ya haberlo hecho con aterioridad no es necesario repetirlo.

## 3) Crear paquete
Ahora dirigete a esa carpeta, una vez dentro de la misma dirigete a la carpeta src:

    cd ~/grupo_03_doosan_m0609_ws/src/

Ahora dentro de src vamos a crear un paquete donde estaran los nodos, para poder hacerlo ejecuta el siguiente comando:

    ros2 pkg create --build-type ament_python grupo_03_doosan_m0609_tasks --dependencies rclpy sensor_msgs geometry_msgs rcl_interfaces tf2_msgs std_msgs

## 4) Copia de archivos importantes
Despues de haber creado el paquete nos dirigiremos nuevamente a la carpeta del clon del repositorio de git:

    cd ~/primer_parcial_grupo3

Una vez dentro copiaremos los codigos de python a la carpeta recien creada, para eso ejecute el siguiente comando:

    cp cinematica_directa.py cinematica_inversa.py ~/grupo_03_doosan_m0609_ws/src/grupo_03_doosan_m0609_tasks/grupo_03_doosan_m0609_tasks/

Ahora copiaremos los archivos shell al workspace, con el siguiente comando:

    cp compilar.sh ejecutar_cd.sh ejecutar_ci.sh abrir.sh ~/grupo_03_doosan_m0609_ws/

Por ultimo abriremos el archivo "setup.txt" (Puedes abrirlo de la forma que quieras ej: nano, gedit, code. Recomiendo usar code para mayor comodidad), y copia todo el codigo en el archivo "setup.py" ubicado en la siguiente direccion:

    cd ~/grupo_03_doosan_m0609_ws/src/grupo_03_doosan_m0609_tasks/

Cuando estes en esa direccion abre "setup.py" y pega el codigo que copiamos anteriormente.

## 5) Abrir Rviz2
Despues vuelve al workspace:

    cd ~/grupo_03_doosan_m0609_ws/

Ahora podras ejecutar el siguiente comando:

    ./abrir.sh 

donde se abrira el rviz con el robot y el joint_state_publisher.

## 6) Compilar
Posterior a eso abre una nueva terminal, sin cerrar la que está corriendo Rviz2, y asegúrate de que sigas en la carpeta "grupo_03_doosan_m0609_ws", después ejecuta este comando:

    ./compilar.sh

Eso te permitira usar los nodos sin muchos problemas. De igual manera solo es necesario usarlo una vez, si no haces nigun cambio en el codigo de los nodos no tienes porque volver a usar este comando.

## 7) Ejecutar nodo de cinemática directa
Ahora ya podrás correr el nodo de cinemática directa ejecutando el siguiente comando:

    ./ejecutar_cd.sh

Este nodo lo que hace es mostrarte continuamente los valores de los angulos de los joints en radianes y la posicion en X, Y y Z del efector final, entonces puedes variar el valor de los angulos con la ventana de joint_state_publisher y veras como cambia en tiempo real, ademas puedes ir al rviz2 para corroborar que la posicion calculada es correcta, cuando quieras dejar de usar el nodo apreta la interrupcion por teclado (ctrl+c).

## 8) Ejecutar nodo de cinematica inversa
Posteriormente para probar este nodo es recomendable cerrar el otro, de igual manera es necesario cerrar la ventana "joint_state_publisher" del rviz2 dado que como es un publicador puede entrar en conflicto con el publicador de este nodo, una vez revisado eso ya podrás correr el nodo de cinemática inversa ejecutando el siguiente comando:

    ./ejecutar_ci.sh

Este nodo lo que esperara es que por otra terminal le mandes las coordenadas de la posicion deseada, para eso abriremos una nueva terminal sin cerrar las otras y ejecutaremos el siguinete comando:

    ros2 topic pub /target geometry_msgs/msg/Point "{x: valor, y: valor, z: valor}" --once

OJO, de ese comando debes modificar donde dice "valor" por la coordenada que quieras que adopte el robot, asegurate de que tu valor sea de tipo flotante y no alteres la sintaxis del comando. Una vez ejecutado ese comando volvemos a la terminal que esta corriendo el nodo de cinematica inversa y podremos ver como nos proporciono la informacion de los angulos hayados, de las iteraciones que le tomo, y el error final. Al final del texto dira que se publico los angulos entonces puedes ir al rviz2 para corroborar que el robot se movio y de igual manera puedes comparar si su posicion es correcta, cuando quieras dejar de usar el nodo apreta la interrupcion por teclado (ctrl+c).
