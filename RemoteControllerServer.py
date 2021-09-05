import pyautogui as g
from time import sleep
import socket as s
from asyncio import *
import re

g.PAUSE=0.01
g.FAILSAFE=False
max_x,max_y=g.size()

# Содаем сокет
serversocket = s.socket(s.AF_INET, s.SOCK_STREAM)
# server_ip = '192.168.100.2'
server_ip = s.gethostbyname(s.gethostname())
set_ip = input(f'Введите ip адрес сервера: \n(по умолчанию: {server_ip}\nдля выбора ip по умолчанию нажмите Enter)\n')
if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',set_ip) :
    server_ip = set_ip
elif set_ip:
    print('Неверный формат ip адреса, использую адрес по умолчанию...')
server_port = 5555
try:
    serversocket.bind((server_ip,server_port))
    serversocket.listen()
    print(f'Сервер запущен!\nip:   {server_ip}\nport: {server_port}')
except Exception:
    print('Недопустимый ip - адрес!\nПосмотрите доступные ip адреса с помощью команды ipconfig в командной строке.')
    exit()


# Подключение клиента
def connect():
    try:
        serversocket.setblocking(True)
        clientsocket, address = serversocket.accept()
        clientsocket.send(b'Connected')
        print(f'Подключен клиент {address}')
        handle_client(clientsocket)
    except ConnectionError:
        print('Ошибка подключения!')
        return


def handle_client(client):
    serversocket.setblocking(False)
    move_step = 10
    while True:
        # Получаем запрос клиента
        try:
            msg = client.recv(1024).decode()
            client.send(b'c')
        except ConnectionError:
            print('Клиент отключен!')
            break
        # Обрабатываем
        x, y = g.position()

        if msg == 'Left':
            if x - move_step >= 0:
                g.moveRel(xOffset=-move_step, yOffset=0, duration=0.01)
        elif msg == 'Right':
            if x + move_step <= max_x:
                g.moveRel(xOffset=move_step, yOffset=0, duration=0.01)
        elif msg == 'Up':
            if y - move_step >= 0:
                g.moveRel(yOffset=-move_step, xOffset=0, duration=0.01)
        elif msg == 'Down':
            if y + move_step <= max_y:
                g.moveRel(yOffset=move_step, xOffset=0, duration=0.01)
        elif msg == 'LeftUp':
            if x - move_step >= 0 and y - move_step >= 0:
                g.moveRel(yOffset=-move_step, xOffset=-move_step, duration=0.01)
        elif msg == 'RightUp':
            if x + move_step <= max_x and y - move_step >= 0:
                g.moveRel(yOffset=-move_step, xOffset=move_step, duration=0.01)
        elif msg == 'LeftDown':
            if x - move_step >= 0 and y + move_step <= max_y:
                g.moveRel(yOffset=move_step, xOffset=-move_step, duration=0.01)
        elif msg == 'RightDown':
            if x + move_step <= max_x and y + move_step <= max_y:
                g.moveRel(yOffset=move_step, xOffset=move_step, duration=0.01)
        elif msg == 'LeftClick':
            g.click()
        elif msg == 'RightClick':
            g.rightClick()
        elif msg == 'ScrollUp':
            g.scroll(move_step)
        elif msg == 'ScrollDown':
            g.scroll(-move_step)
        elif re.match('Sense:*',msg):
            move_step = int(msg.split()[1])
        else:
            continue
    return


if __name__ == '__main__':
    while True:
        connect()
