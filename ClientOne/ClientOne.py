import json
import socket

import jsonschema
from jsonschema import validate

win_schema = {
    "type": "object",
    "properties": {
        'speed': {
            'type': 'string'
        }
    }
}


def client_program():
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))
    print('Добро пожаловать в игру!\n' +
          'Вы играете за оператора. Для того, чтобы получить информацию о карабле введите <get info>.\n' +
          'Для того, чтобы завершить игру введите <close>. Любое другое сообщение будет отправлено летчику\n' +
          'как инструкции с действию. Вам доступна информация о расстоянии до космической станции, скорости \n' +
          'корабля относительно станции, скорости вращения корабля и станции и угловой параметр стыковки. \n' +
          'Для победы необходимо, чтобы совпадали скорости вращения корабля и станции, чтобы скорость \n' +
          'корабля относительно станции в момент стыковки была не больше 10 и чтобы угловой параметр \n' +
          'стыковки был не больше 10 градусов.')
    try:
        while True:
            message = input(" Запросить данные или сделать приказ летчику -> ")
            json_str = {
                'instruction': message
            }
            client_socket.send(json.dumps(json_str).encode())
            if message == "close":
                break
            data = client_socket.recv(1024).decode()
            message = json.loads(data)
            try:
                validate(message, win_schema)
                print(str(message['win']))
                break
            except jsonschema.exceptions.ValidationError:
                print('Данные о корабле:')
                print('Расстояние: ' + str(message['distance']) + '; '
                      + 'Скорость: ' + str(message['speed']) + '; '
                      + 'Вращение: ' + str(message['rotation']) + '; '
                      + 'Вращение станции: ' + str(message['rotationStation']) + '; '
                      + 'Угловой параметр: ' + str(message['dockingParam']) + '°.')
    except BaseException:
        print("Обрыв соединения")
        client_socket.close()


if __name__ == '__main__':
    client_program()
