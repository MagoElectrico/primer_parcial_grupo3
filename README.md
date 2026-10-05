# primer_parcial_grupo3
Repositorio del primer parcial del grupo 3 de robotica simulacion de cinematica directa e inversa del robot doosan_m0609.

## 1) Clonar el repositorio 
Al clonar el repositorio tendras la carpeta "primer_parcial_grupo3". Dentro de esa carpeta estara otra carpeta llamada "grupo_03_doosan_m0609_ws" donde estan todos los archivos necesarios.

## 2) instalar el entorno
Entra a la carpeta "grupo_03_doosan_m0609_ws" y dale permisos a los archivos shell de la siguiente manera:

- sudo chmod 777 instalar.sh
- sudo chmod 777 abrir.sh
- sudo chmod 777 compilar.sh
- sudo chmod 777 ejecutar_cd.sh
- sudo chmod 777 ejecutar_ci.sh

una vez hecho eso ejecuta el siguiente comando:

- ./instalar.sh

y espera que se instale todo. Solo es necesario usar una vez este comando, si ya lo hiciste no lo hagas otra vez.

## 3) Abrir Rviz2
Posteriormente ejecuta el comando:

- ./abrir.sh 

donde se abrira el rviz con el robot y el joint_state_publisher. Para poder ejecutar los nodos de cinematica inversa y directa tienes que cerrar la ventana que se llama joint_state_publisher dado que este es un publicador y no se podra ejecutar el nodo.

## 4) Compilar
Posterior a eso abre una nueva terminal, sin cerrar la que esta corriendo rviz, y asegurate de que sigas en la carpeta "grupo_03_doosan_m0609_ws", depues ejecuta este comando:

- ./compilar.sh

## 5) Ejecutar nodo de cinematica directa
Ahora ya podrás correr el nodo de cinematica directa ejecutando el siguiente comando:

- ./ejecutar_cd.sh

despues te pedira que pongas angulos en grados para cada joint y te dara la posicion alcanzada en x, y, z, lo puedes verificar en rviz que el robot se movio y tambien puedes verificar las coordenadas en rviz, veras al costado una ventana que dice displays, ahi veras un apartado que dice TF dentro de este otro que dice link6 y finalmente podrás ver la posicion, podras hacer esto indefinidamente hasta que hagas la interrupcion por teclado "crtl+c".

## 6) Ejecutar nodo de cinematica inversa
Posteriormente para probar este nodo tienes que cerrar el otro, asegurate de tener el nodo cerrado y que puedas escribir en la terminal, una vez revisado eso ya podras correr el nodo de cinematica inversa ejecutando el siguiente comando:

- ./ejecutar_ci.sh

despues te pedira que pongas las coordenadas x,y,z deseadas y te dara los ángulos que le corresponden a cada joint a lo puedes verificar en rviz que el robot se movio y tambien puedes verificar las coordenadas en rviz, veras al costado una ventana que dice displays, ahi veras un apartado que dice TF dentro de este otro que dice link6 y finalmente podrás ver la posicion, podras hacer esto indefinidamente hasta que hagas la interrupcion por teclado "crtl+c".
