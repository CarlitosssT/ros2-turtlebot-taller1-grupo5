#!/usr/bin/env python3
import time
import curses

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleBotTeleop(Node):
    def __init__(self, stdscr):
        super().__init__('turtle_bot_teleop')

        # Velocidades fijas
        self.V_LIN = 0.20
        self.V_ANG = 0.80

        self.pub = self.create_publisher(Twist, '/turtlebot_cmdVel', 10)

        # curses setup
        self.stdscr = stdscr
        self.stdscr.nodelay(True)      # no bloquear
        self.stdscr.keypad(True)
        curses.curs_set(0)

        self.last_key_time = time.time()
        self.cmd = Twist()

        self.get_logger().info("Teleop (curses) listo.")
        self._draw_help()

        # Timer ROS
        self.timer = self.create_timer(0.05, self._loop)  # 20 Hz

    def _draw_help(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Teleop TurtleBot2 (Grupo 5)")
        self.stdscr.addstr(2, 0, "Controles: w=adelante, s=atras, a=izq, d=der, ESPACIO=stop, q=salir")
        self.stdscr.addstr(4, 0, f"Velocidades fijas: V_LIN={self.V_LIN} m/s, V_ANG={self.V_ANG} rad/s")
        self.stdscr.addstr(6, 0, "TIP: asegúrate de tener foco en esta terminal.")
        self.stdscr.refresh()

    def _set_cmd(self, v, w):
        msg = Twist()
        msg.linear.x = float(v)
        msg.angular.z = float(w)
        self.cmd = msg

    def _loop(self):
        # leer tecla sin bloquear
        try:
            ch = self.stdscr.getch()
        except Exception:
            ch = -1

        if ch != -1:
            self.last_key_time = time.time()

            if ch in (ord('w'), ord('W')):
                self._set_cmd(self.V_LIN, 0.0)
            elif ch in (ord('s'), ord('S')):
                self._set_cmd(-self.V_LIN, 0.0)
            elif ch in (ord('a'), ord('A')):
                self._set_cmd(0.0, self.V_ANG)
            elif ch in (ord('d'), ord('D')):
                self._set_cmd(0.0, -self.V_ANG)
            elif ch == ord(' '):
                self._set_cmd(0.0, 0.0)
            elif ch in (ord('q'), ord('Q')):
                # stop y salir
                self._set_cmd(0.0, 0.0)
                self.pub.publish(self.cmd)
                raise SystemExit

        # watchdog: si no se presiona nada, frena
        if (time.time() - self.last_key_time) > 0.25:
            self._set_cmd(0.0, 0.0)

        self.pub.publish(self.cmd)


def main():
    # IMPORTANTE: curses.wrapper se encarga de restaurar el terminal SIEMPRE
    def _wrapped(stdscr):
        rclpy.init()
        node = TurtleBotTeleop(stdscr)
        try:
            rclpy.spin(node)
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            # stop final
            try:
                node.pub.publish(Twist())
            except Exception:
                pass
            node.destroy_node()
            rclpy.shutdown()

    curses.wrapper(_wrapped)


if __name__ == '__main__':
    main()
