import json
import socket


win_schema = {
    "type": "object",
    "properties": {
        'speed': {
            'type': 'string'
        }
    }
}

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    print('Добро пожаловать в игру!\n' +
          'Вы играете за летчика. Вам будет приходить реководство к действию от оператора. По нему вы долж-\n' +
          'ны изменить скорость корабля относительно станции и скорость вращения корабля.')
    try:
        while True:
            data = client_socket.recv(1024).decode()
            recvMessage = json.loads(data)['instruction']
            if recvMessage == "close":
                print('Оператор прекратил игру.')
                break
            if recvMessage == "You win!" or recvMessage == "You lost.":
                print(recvMessage)
                break
            print('Указание от оператора: ' + recvMessage)
            newSpeed = input(" input new speed -> ")
            newRotation = input(" input new rotation -> ")
            json_string = {
                'newSpeed': newSpeed,
                'newRotation': newRotation
            }
            client_socket.send((json.dumps(json_string)).encode())  # send message
    except BaseException:
        print("Обрыв соединения")
        client_socket.close()


if __name__ == '__main__':
    client_program()
