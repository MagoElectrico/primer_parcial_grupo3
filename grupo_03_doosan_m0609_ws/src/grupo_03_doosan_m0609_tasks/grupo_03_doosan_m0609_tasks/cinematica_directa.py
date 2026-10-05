import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import numpy as np
import sympy as sp

class CinematicaDirecta_node(Node):
    def __init__(self):
        super().__init__('cinematica_directa_node')
        self.publisher=self.create_publisher(
            JointState,
            '/joint_states',
            10
        )
        self.timer=self.create_timer(
            0.1,
            self.timer_callback
        )
        self.get_logger().info(
            'cinematica directa node listo'
        )
    
    def timer_callback(self):
        joint_state=JointState()
        joint_state.header.stamp=self.get_clock().now().to_msg()
        joint_state.name=['joint_1','joint_2','joint_3', 'joint_4','joint_5','joint_6']
        print('A continuacion ingrese los valores de los angulos articulares en grados: \n')
        theta_1=float(input("Ingrese el valor de theta 1: "))
        t1 = np.radians(theta_1)
        theta_2=float(input("Ingrese el valor de theta 2: "))
        t2 = np.radians(theta_2)
        theta_3=float(input("Ingrese el valor de theta 3: "))
        t3 = np.radians(theta_3)
        theta_4=float(input("Ingrese el valor de theta 4: "))
        t4 = np.radians(theta_4)
        theta_5=float(input("Ingrese el valor de theta 5: "))
        t5 = np.radians(theta_5)
        theta_6=float(input("Ingrese el valor de theta 6: "))
        t6 = np.radians(theta_6)
        if -6.283<=t1<=6.283 and -6.283<=t2<=6.283 and -2.618<=t3<=2.618 and -6.283<=t4<=6.283 and -6.283<=t5<=6.283 and -6.283<=t6<=6.283:
            joint_state.position=[t1,t2,t3,t4,t5,t6]
            self.publisher.publish(joint_state)

            a1=0.134
            a2=0.0062
            a3=0.409
            a5=0.368
            a6=0.121
            
            A12 = sp.Matrix([
                [sp.cos(t1), 0, -sp.sin(t1), 0],
                [sp.sin(t1), 0,  sp.cos(t1), 0],
                [0,        -1, 0, a1],
                [0,         0, 0, 1]
            ])

            A23 = sp.Matrix([
                [sp.sin(t2),  sp.cos(t2), 0, a3*sp.sin(t2)],
                [-sp.cos(t2), sp.sin(t2), 0, -a3*sp.cos(t2)],
                [0,           0,          1, a2],
                [0,           0,          0, 1]
            ])

            A34 = sp.Matrix([
                [-sp.sin(t3), 0, sp.cos(t3), 0],
                [ sp.cos(t3), 0, sp.sin(t3), 0],
                [0,           1, 0, 0],
                [0,           0, 0, 1]
            ])

            A45 = sp.Matrix([
                [sp.cos(t4), 0, -sp.sin(t4), 0],
                [sp.sin(t4), 0,  sp.cos(t4), 0],
                [0,         -1, 0, a5],
                [0,          0, 0, 1]
            ])

            A56 = sp.Matrix([
                [sp.cos(t5), 0, -sp.sin(t5), 0],
                [sp.sin(t5), 0,  sp.cos(t5), 0],
                [0,         -1, 0, 0],
                [0,          0, 0, 1]
            ])

            A67 = sp.Matrix([
                [sp.cos(t6), sp.sin(t6), 0, 0],
                [sp.sin(t6), -sp.cos(t6), 0, 0],
                [0, 0, -1, -a6],
                [0, 0, 0, 1]
            ])

            A07 = A12 * A23 * A34 * A45 * A56 * A67

            self.get_logger().info(
                f'La posicion del efector final es: '
                f'X: {A07[0,3]} '
                f'Y: {A07[1,3]} '
                f'Z: {A07[2,3]} '
            )
        else:
            self.get_logger().info(
                'Los valores de los angulos articulares estan fuera del rango permitido'
            )

def main(args=None):
    rclpy.init(args=args)
    node=CinematicaDirecta_node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
