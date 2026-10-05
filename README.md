# Primer_parcial_grupo3
Repositorio del primer parcial del grupo 3 de robótica simulación de cinemática directa e inversa del robot doosan_m0609.

## 1) Clonar el repositorio 
Al clonar el repositorio tendras la carpeta "primer_parcial_grupo3". Dentro de esa carpeta se encuentra otra carpeta llamada "grupo_03_doosan_m0609_ws" donde están todos los archivos necesarios.

## 2) Instalar el entorno
Entra a la carpeta "grupo_03_doosan_m0609_ws" y dale permisos a los archivos shell de la siguiente manera:

    sudo chmod 777 instalar.sh
    sudo chmod 777 abrir.sh
    sudo chmod 777 compilar.sh
    sudo chmod 777 ejecutar_cd.sh
    sudo chmod 777 ejecutar_ci.sh

una vez hecho eso ejecuta el siguiente comando:

    ./instalar.sh

y espera que se instale todo. Solo es necesario usar una vez este comando, si ya lo hiciste no lo hagas otra vez.

## 3) Abrir Rviz2
Posteriormente ejecuta el comando:

    ./abrir.sh 

donde se abrira el rviz con el robot y el joint_state_publisher. Para poder ejecutar los nodos de cinemática inversa y directa tienes que cerrar la ventana que se llama joint_state_publisher dado que este es un publicador y no se podrá ejecutar el nodo.

## 4) Compilar
Posterior a eso abre una nueva terminal, sin cerrar la que está corriendo Rviz2, y asegúrate de que sigas en la carpeta "grupo_03_doosan_m0609_ws", después ejecuta este comando:

    ./compilar.sh

## 5) Ejecutar nodo de cinemática directa
Ahora ya podrás correr el nodo de cinemática directa ejecutando el siguiente comando:

    ./ejecutar_cd.sh

Después, el programa te pedirá que ingreses los ángulos en grados correspondientes a cada joint. Una vez ingresados, mostrará la posición alcanzada por el robot en los ejes X, Y y Z.
Puedes verificar que el robot se haya movido correctamente en RViz2, así como comprobar las coordenadas alcanzadas. En la ventana lateral Displays, encontrarás el apartado TF. Dentro de este, selecciona Frames, luego link6 y finalmente Position. Allí podrás visualizar la posición actual del efector final en los ejes X, Y y Z.
Este procedimiento puede repetirse indefinidamente para probar diferentes configuraciones articulares. El programa continuará ejecutándose hasta que realices una interrupción por teclado con "ctrl+C".

## 6) Ejecutar nodo de cinematica inversa
Posteriormente para probar este nodo tienes que cerrar el otro, asegúrate de tener el nodo cerrado y que puedas escribir en la terminal, una vez revisado eso ya podrás correr el nodo de cinemática inversa ejecutando el siguiente comando:

    ./ejecutar_ci.sh

Después, el programa te pedirá que ingreses la posición deseada en X, Y y Z. Una vez ingresada, mostrará los ángulos en grados correspondientes a cada joint.
Puedes verificar que el robot se haya movido correctamente en RViz2, así como comprobar las coordenadas alcanzadas con los ángulos hallados. En la ventana lateral Displays, encontrarás el apartado TF. Dentro de este, selecciona Frames, luego link6 y finalmente Position. Allí podrás visualizar la posición actual del efector final en los ejes X, Y y Z.
Este procedimiento puede repetirse indefinidamente para probar diferentes configuraciones articulares. El programa continuará ejecutándose hasta que realices una interrupción por teclado con "ctrl+C".
