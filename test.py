import os
import sys
import json
import math
import socket
import time
import threading
import struct


def truncate(number, digits):
    # 소수점 digits 자리 이후 값 버림
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def binder(client_socket, addr):
    sys.path.append(
        "/var/app/venv/staging-LQM1lest/lib/python3.8/site-packages")
    sys.path.append("../")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    try:
        while True:
            receive_data = client_socket.recv(73)
            if not receive_data:
                print(addr, "to quit!")
                print("Waiting for next data...")
                break
            print(len(receive_data))
            msg = receive_data.hex()
            print("data received!!", time.strftime(
                '%Y-%m-%d'), time.strftime('%H:%M:%S'))

            if msg:
                print('Received from', addr, msg)
                buoy_id = int(msg[:8], 16)
                battery = int(msg[8:10], 16)
                lat = int(msg[10:18], 16)/1000000
                lon = int(msg[18:26], 16)/1000000
                # print("lat : ", lat)
                # print("lat round plus : ", round(lat + 0.0002, 5))
                # print("lat round minus : ", round(lat - 0.0002, 5))
                # print('lon : ', lon)
                # print("lon round plus : ", round(lon + 0.0002, 5))
                # print('lon round minus : ', round(lon - 0.0002, 5))

                sensor1_temp = struct.unpack(
                    '!f', bytes.fromhex(msg[26:34]))[0]
                sensor1_oxy_per = struct.unpack(
                    '!f', bytes.fromhex(msg[34:42]))[0]
                sensor1_oxy_mpl = struct.unpack(
                    '!f', bytes.fromhex(msg[42:50]))[0]
                sensor1_oxy_ppm = struct.unpack(
                    '!f', bytes.fromhex(msg[50:58]))[0]

                sensor2_temp = struct.unpack(
                    '!f', bytes.fromhex(msg[58:66]))[0]
                sensor2_ph = struct.unpack('!f', bytes.fromhex(msg[66:74]))[0]
                sensor2_redox = struct.unpack(
                    '!f', bytes.fromhex(msg[74:82]))[0]
                sensor2_ph_meter = struct.unpack(
                    '!f', bytes.fromhex(msg[82:90]))[0]

                sensor3_temp = struct.unpack(
                    '!f', bytes.fromhex(msg[90:98]))[0]
                sensor3_conduct = struct.unpack(
                    '!f', bytes.fromhex(msg[98:106]))[0]
                sensor3_salt = struct.unpack(
                    '!f', bytes.fromhex(msg[106:114]))[0]
                sensor3_tds = struct.unpack(
                    '!f', bytes.fromhex(msg[114:122]))[0]

                chlorophy = int(msg[122:126], 16) / \
                    (10 ** int(msg[126:130], 16))

                chlorophy_temp = int(msg[130:134], 16) / \
                    (10 ** int(msg[134:138], 16))

                modbus_crc = str(msg[138:142])

                print('buoy_id : ', buoy_id)
                print('battery : ', battery)
                print('lat : ', lat)
                print('lon : ', lon)

                print('sensor1_temp : ', sensor1_temp)
                print('sensor1_oxy_per : ', sensor1_oxy_per)
                print('sensor1_oxy_mpl : ', sensor1_oxy_mpl)
                print('sensor1_oxy_ppm : ', sensor1_oxy_ppm)

                print('sensor2_temp : ', sensor2_temp)
                print('sensor2_ph : ', sensor2_ph)
                print('sensor2_redox : ', sensor2_redox)
                print('sensor2_ph_meter : ', sensor2_ph_meter)

                print('sensor3_temp : ', sensor3_temp)
                print('sensor3_conduct : ', sensor3_conduct)
                print('sensor3_salt : ', sensor3_salt)
                print('sensor3_tds : ', sensor3_tds)

                print('chlorophy : ', chlorophy)
                print('chlorophy_temp : ', chlorophy_temp)

                print('modbus_crc', modbus_crc)

            length = len(receive_data)
            client_socket.sendall(length.to_bytes(4, byteorder="big"))
            client_socket.sendall(receive_data)

            # msg = "echo : " + msg
            # echo_msg = msg.encode()

            # length = len(echo_msg)

            # client_socket.sendall(length.to_bytes(4, byteorder="big"))
            # client_socket.sendall(echo_msg)
            # print(echo_msg)

    except ConnectionResetError as e:
        print(e, addr)

    finally:
        print("client socket close!!")
        client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('172.30.1.35', 6557))
# server_socket.bind(('172.30.1.33', 6557))

server_socket.listen()
print('Server start up!')

try:
    while True:
        print('Receiving data...')
        client_socket, addr = server_socket.accept()
        th = threading.Thread(target=binder, args=(client_socket, addr))
        th.start()
        print("Device address : ", addr)
except socket.error as e:
    print(e)

finally:
    print("server socket close!!")
    server_socket.close()
