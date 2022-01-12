import socket
import time
import json
import jsonschema
import numpy as np
from jsonschema import validate

speed = 1000
distance = 1000
rotation = 1000
rotationStation = 500
dockingParam = 100


saving_schema = {
    "type": "object",
    "properties": {
        'speed': {
            'type': 'number',
            'minimum': 0
        },
        'distance': {
            'type': 'number',
            'minimum': 0
        },
        'rotation': {
            'type': 'number'
        },
        'rotationStation': {
            'type': 'number'
        },
        'dockingParam': {
            'type': 'number',
            'minimum': 0,
            'maximum': 360
        }
    }
}


def server_program():
    global distance
    global rotationStation
    global speed
    global rotation
    global dockingParam
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    connOne, clientOne = server_socket.accept()
    connTwo, clientTwo = server_socket.accept()

    with open('saving.json', encoding='utf-8') as file:
        saving = json.load(file)
        print(saving)
        try:
            validate(saving, saving_schema)
        except jsonschema.exceptions.ValidationError:
            print("Ошибка валидации")
            return
        speed = saving['speed']
        distance = saving['distance']
        rotation = saving['rotation']
        rotationStation = saving['rotationStation']
        dockingParam = saving['dockingParam']

    startTime = time.time()
    while True:
        data, address = connOne.recvfrom(1024)
        time.sleep(1)
        data = json.loads(data.decode())
        print(data)
        if not data['instruction']:
            break
        if data['instruction'] == "get info":
            thisTime = time.time()
            distance = distance - speed * (thisTime - startTime) / 3600
            dockingParam = (dockingParam + (np.abs(rotation - rotationStation) * 180 * (thisTime - startTime) / np.pi)) % 360
            startTime = time.time()

            if distance < 0:
                with open('saving.json', 'w', encoding='utf-8') as file:
                    json.dump({'speed': 1000, 'distance': 1000, 'rotation': 100, 'rotationStation': 50, 'dockingParam': 180}, file)
                if (rotation == rotationStation) and (speed <= 10) and dockingParam < 10:
                    json_str = {'win': 'You win!'}
                    connOne.send(json.dumps(json_str).encode())
                    json_str = {'instruction': 'You win!'}
                    connTwo.send(json.dumps(json_str).encode())
                else:
                    json_str = {'win': 'You lost.'}
                    connOne.send(json.dumps(json_str).encode())
                    json_str = {'instruction': 'You lost.'}
                    connTwo.send(json.dumps(json_str).encode())
                break
            json_string = {
                'distance': distance,
                'speed': speed,
                'rotation': rotation,
                'rotationStation': rotationStation,
                'dockingParam': dockingParam
            }
            connOne.send(json.dumps(json_string).encode())
        elif data['instruction'] == "close":
            connTwo.send(json.dumps(data).encode())
            break
        else:
            connTwo.send(json.dumps(data).encode())
            data, address = connTwo.recvfrom(1024)
            thisTime = time.time()
            distance = distance - speed * (thisTime - startTime) / 3600
            dockingParam = (dockingParam + (np.abs(rotation - rotationStation) * 180 * (thisTime - startTime) / np.pi)) % 360
            startTime = time.time()
            time.sleep(1)
            message = json.loads(data.decode())
            print(message)
            speed = float(message['newSpeed'])
            rotation = float(message['newRotation'])
            with open('saving.json', 'w', encoding='utf-8') as file:
                json.dump(
                    {'speed': speed, 'distance': distance, 'rotation': rotation, 'rotationStation': rotationStation, 'dockingParam': dockingParam},
                    file)
            json_string = {
                'distance': distance,
                'speed': speed,
                'rotation': rotation,
                'rotationStation': rotationStation,
                'dockingParam': dockingParam
            }
            connOne.send(json.dumps(json_string).encode())

    connOne.close()
    connTwo.close()


if __name__ == '__main__':
    server_program()
