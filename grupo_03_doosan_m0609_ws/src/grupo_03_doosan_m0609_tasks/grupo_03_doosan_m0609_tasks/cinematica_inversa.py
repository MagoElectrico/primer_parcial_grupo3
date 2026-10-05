import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import numpy as np
import sympy as sp


class CinematicaInversaNode(Node):

    def __init__(self):

        super().__init__('cinematica_inversa_node')

        self.publisher = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.timer_callback
        )


    def timer_callback(self):

        t1, t2, t3, t4, t5, t6 = sp.symbols(
            'theta1 theta2 theta3 theta4 theta5 theta6',
            real=True
        )

        self.q = [t1, t2, t3, t4, t5, t6]

        d1 = sp.Rational('0.134')
        d2 = sp.Rational('0.0062')
        a3 = sp.Rational('0.409')
        d5 = sp.Rational('0.368')
        d6 = sp.Rational('0.121')

        

        Px = (
            -d6 * sp.sin(t1) * sp.sin(t4) * sp.sin(t5)
            -d2 * sp.sin(t1)
            +a3 * sp.sin(t2) * sp.cos(t1)
            +d6 * sp.sin(t5) * sp.cos(t1)
                * sp.cos(t4) * sp.cos(t2 + t3)
            +d6 * sp.sin(t2 + t3)
                * sp.cos(t1) * sp.cos(t5)
            +d5 * sp.sin(t2 + t3) * sp.cos(t1)
        )

        Py = (
            a3 * sp.sin(t1) * sp.sin(t2)
            +d6 * sp.sin(t1) * sp.sin(t5)
                * sp.cos(t4) * sp.cos(t2 + t3)
            +d6 * sp.sin(t1) * sp.sin(t2 + t3)
                * sp.cos(t5)
            +d5 * sp.sin(t1) * sp.sin(t2 + t3)
            +d6 * sp.sin(t4) * sp.sin(t5) * sp.cos(t1)
            +d2 * sp.cos(t1)
        )

        Pz = (
            -d6 * sp.sin(t5) * sp.sin(t2 + t3)
                * sp.cos(t4)
            +a3 * sp.cos(t2)
            +d6 * sp.cos(t5) * sp.cos(t2 + t3)
            +d5 * sp.cos(t2 + t3)
            +d1
        )

        self.P = sp.Matrix([
            Px,
            Py,
            Pz
        ])
        
        self.J_v = self.P.jacobian(self.q)

        self.J_v = self.J_v.applyfunc(
            sp.trigsimp
        )
        
        self.P_func = sp.lambdify(
            self.q,
            self.P,
            'numpy'
        )

        self.J_func = sp.lambdify(
            self.q,
            self.J_v,
            'numpy'
        )
        
        print("Ingrese la posición deseada del efector final")
        x=float(input("Ingrese el valor de x: "))
        y=float(input("Ingrese el valor de y: "))
        z=float(input("Ingrese el valor de z: "))

        self.Pd = np.array([
            x,
            y,
            z
        ], dtype=float)

        self.q_actual = np.array([
            np.deg2rad(10),
            np.deg2rad(20),
            np.deg2rad(30),
            np.deg2rad(40),
            np.deg2rad(50),
            np.deg2rad(60)
        ], dtype=float)

        limites_min = np.array([
            -6.283,
            -6.283,
            -2.618,
            -6.283,
            -6.283,
            -6.283
        ])

        limites_max = np.array([
            6.283,
            6.283,
            2.618,
            6.283,
            6.283,
            6.283
        ])

        max_iter = 100
        tolerancia = 1e-6
        alpha = 0.5

        convergio = False

        for i in range(max_iter):

            P_actual = np.array(
                self.P_func(*self.q_actual),
                dtype=float
            ).flatten()

            error = self.Pd - P_actual
            
            error_norma = np.linalg.norm(error)

            if error_norma < tolerancia:
                convergio = True
                break

            J_actual = np.array(
                self.J_func(*self.q_actual),
                dtype=float
            )

            J_pinv = np.linalg.pinv(J_actual)

            delta_q = alpha * J_pinv @ error

            self.q_actual = self.q_actual + delta_q

            self.q_actual = np.clip(
                self.q_actual,
                limites_min,
                limites_max
            )

        
        self.iteraciones = i + 1

        self.P_final = np.array(
            self.P_func(*self.q_actual),
            dtype=float
        ).flatten()

        self.error_final = self.Pd - self.P_final
    
        if convergio:
            print("\n La cinemática inversa convergió.")
            print(f"\nIteraciones realizadas: {self.iteraciones}")


            for j, angulo in enumerate(self.q_actual):
                self.get_logger().info(
                    f"q{j + 1} = {angulo:.4f} rad, {np.degrees(angulo):.2f}°"
                )
        

            self.get_logger().info(
                f"Posición deseada: X = {self.Pd[0]:.6f} m, Y = {self.Pd[1]:.6f} m, Z = {self.Pd[2]:.6f} m"
            )

            self.get_logger().info(
                f"Posición obtenida teoricamente: X = {self.P_final[0]:.6f} m, Y = {self.P_final[1]:.6f} m, Z = {self.P_final[2]:.6f} m"
            )

            self.primera_publicacion = True


            joint_state = JointState()

            joint_state.header.stamp = (
                self.get_clock().now().to_msg()
            )

            joint_state.name = [
                'joint_1',
                'joint_2',
                'joint_3',
                'joint_4',
                'joint_5',
                'joint_6'
            ]

            joint_state.position = self.q_actual.tolist()
            self.publisher.publish(joint_state)
        else:
            print("\n No se alcanzó la tolerancia.")

        


def main(args=None):

    rclpy.init(args=args)
    node = CinematicaInversaNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
