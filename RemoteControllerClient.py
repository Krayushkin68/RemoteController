import socket
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivymd.theming import ThemeManager
import time


class RemoteControllerClient(MDApp):
    command = ''
    state = ''
    drag = 'DragOff'
    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Gray'
        self.sm = ScreenManager()
        self.sm.add_widget(ConnectScreen(name='connect'))
        self.sm.add_widget(ControlScreen(name='control'))
        Clock.schedule_interval(self.checker, 1.0 / 60)  # 20 FPS
        return self.sm

    def set_sense(self, sense):
        command = f'Sense: {sense}'
        self.send_command(command)

    def set_screen(self, name_screen):
        self.sm.current = name_screen

    def set_command(self, comm):
        self.command = comm
        self.state = 'down'

    def set_state(self, state):
        self.state = state

    def checker(self, _):
        if self.state == 'down' and self.command:
            self.send_command(self.command)


    # def set_drag(self):
    #     if self.drag == 'DragOff':
    #         self.drag = 'DragOn'
    #         self.sm.current_screen.ids.drag_btn.md_bg_color = [0.6, 0.6, 0.6, 1]
    #         self.send_command(self.drag)
    #     elif self.drag == 'DragOn':
    #         self.drag = 'DragOff'
    #         self.sm.current_screen.ids.drag_btn.md_bg_color = [0.9, 0.9, 0.9, 1]
    #         self.send_command(self.drag)

    def back(self):
        self.set_screen("connect")
        self.socket.close()

    def connect_server(self,server_ip,server_port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((server_ip, int(server_port)))
            accept_msg = self.socket.recv(1024).decode()
            if accept_msg == 'Connected':
                # print('Успешное подключение')
                self.set_screen('control')
            else:
                self.set_screen('connect')
        except ConnectionError:
            # print('Ошибка подключения')
            self.socket.close()
            self.set_screen('connect')
        except Exception:
            self.socket.close()
            self.set_screen('connect')

    def send_command(self, command):
        try:
            self.socket.send(command.encode())
        except ConnectionError:
            self.socket.close()
            self.set_screen('connect')


class ConnectScreen(MDScreen):
    pass


class ControlScreen(MDScreen):
    pass


if __name__ == '__main__':
    RemoteControllerClient().run()
