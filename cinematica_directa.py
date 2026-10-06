import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import numpy as np


class CinematicaDirectaNode(Node):

    def __init__(self):
        super().__init__('cinematica_directa_node')

        # Suscripción a /joint_states
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        self.get_logger().info(
            'Nodo de cinemática directa iniciado. '
            'Esperando datos de /joint_states...'
        )




    # ---------------------------------------------------------
    # Callback de /joint_states
    # ---------------------------------------------------------
    def joint_state_callback(self, msg):

        # Verificar que llegaron las 6 articulaciones
        nombres_requeridos = [
            'joint_1',
            'joint_2',
            'joint_3',
            'joint_4',
            'joint_5',
            'joint_6'
        ]

        joint_map = dict(zip(msg.name, msg.position))

        for nombre in nombres_requeridos:

            if nombre not in joint_map:

                self.get_logger().warn(
                    f'No se encontró {nombre} en /joint_states'
                )

                return

        # -----------------------------------------------------
        # Orden correcto de las articulaciones
        # -----------------------------------------------------

        t1 = joint_map['joint_1']
        t2 = joint_map['joint_2']
        t3 = joint_map['joint_3']
        t4 = joint_map['joint_4']
        t5 = joint_map['joint_5']
        t6 = joint_map['joint_6']

        # -----------------------------------------------------
        # Parámetros obtenidos de las matrices DH
        # -----------------------------------------------------

        a1 = 0.134
        a2 = 0.0062
        a3 = 0.409
        a5 = 0.368
        a6 = 0.121

        # -----------------------------------------------------
        # Matrices homogéneas DH
        # Se mantienen exactamente según tu modelo
        # -----------------------------------------------------

        A12 = np.array([
            [np.cos(t1), 0, -np.sin(t1), 0],
            [np.sin(t1), 0,  np.cos(t1), 0],
            [0,        -1, 0, a1],
            [0,         0, 0, 1]
        ])

        A23 = np.array([
            [np.sin(t2),  np.cos(t2), 0, a3 * np.sin(t2)],
            [-np.cos(t2), np.sin(t2), 0, -a3 * np.cos(t2)],
            [0,           0,          1, a2],
            [0,           0,          0, 1]
        ])

        A34 = np.array([
            [-np.sin(t3), 0, np.cos(t3), 0],
            [ np.cos(t3), 0, np.sin(t3), 0],
            [0,           1, 0, 0],
            [0,           0, 0, 1]
        ])

        A45 = np.array([
            [np.cos(t4), 0, -np.sin(t4), 0],
            [np.sin(t4), 0,  np.cos(t4), 0],
            [0,         -1, 0, a5],
            [0,          0, 0, 1]
        ])

        A56 = np.array([
            [np.cos(t5), 0, -np.sin(t5), 0],
            [np.sin(t5), 0,  np.cos(t5), 0],
            [0,         -1, 0, 0],
            [0,          0, 0, 1]
        ])

        A67 = np.array([
            [np.cos(t6), np.sin(t6), 0, 0],
            [np.sin(t6), -np.cos(t6), 0, 0],
            [0, 0, -1, -a6],
            [0, 0, 0, 1]
        ])

        # -----------------------------------------------------
        # CINEMÁTICA DIRECTA
        # -----------------------------------------------------

        T02 = A12
        T03 = T02 @ A23
        T04 = T03 @ A34
        T05 = T04 @ A45
        T06 = T05 @ A56
        T07 = T06 @ A67

        # -----------------------------------------------------
        # Posición del efector final
        # -----------------------------------------------------

        x = T07[0, 3]
        y = T07[1, 3]
        z = T07[2, 3]

        self.get_logger().info(
            '\n'
            f'q1 = {t1:.2f} rad\n'
            f'q2 = {t2:.2f} rad\n'
            f'q3 = {t3:.2f} rad\n'
            f'q4 = {t4:.2f} rad\n'
            f'q5 = {t5:.2f} rad\n'
            f'q6 = {t6:.2f} rad\n'
            f'X = {x:.6f} m\n'
            f'Y = {y:.6f} m\n'
            f'Z = {z:.6f} m\n'
        )


def main(args=None):

    rclpy.init(args=args)

    node = CinematicaDirectaNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
