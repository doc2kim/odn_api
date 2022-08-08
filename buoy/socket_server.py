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

    import django
    django.setup()

    from django.core.exceptions import ImproperlyConfigured
    from django.conf import settings

    secrets_file = os.path.join("/var/app/current", 'secrets.json')

    with open(secrets_file) as f:
        secrets = json.loads(f.read())

    def get_secret(setting, secrets=secrets):
        try:
            return secrets[setting]
        except KeyError:
            error_msg = "Set the {} environment variable".format(setting)
            raise ImproperlyConfigured(error_msg)

    settings.DATABASES["default"]['HOST'] = get_secret("RDS_HOST")
    settings.DATABASES["default"]["NAME"] = get_secret("RDS_NAME")
    settings.DATABASES["default"]["USER"] = get_secret("RDS_USER")
    settings.DATABASES["default"]["PASSWORD"] = get_secret("RDS_PASSWORD")
    settings.DATABASES["default"]["PORT"] = get_secret("RDS_PORT")

    from buoy.models import Buoy, Location, Measure, Sensor1, Sensor2, Sensor3
    now = time

    try:
        while True:
            receive_data = client_socket.recv(63)
            if not receive_data:
                print(addr, "to quit!")
                print("Waiting for next data...")
                break

            msg = receive_data.hex()
            print("data received!!", time.strftime(
                '%Y-%m-%d'), time.strftime('%H:%M:%S'))

            if msg:
                print('Received from', addr, msg)

                buoy_id = int(msg[:8], 16)
                battery = int(msg[8:10], 16)

# lon = truncate(int(msg[18: 26], 16)/1000000, 4)

                lat = int(msg[10:18], 16)/1000000
                lon = int(msg[18:26], 16)/1000000
                print("lat : ", lat)
                print("lat round plus : ", round(lat + 0.0002, 5))
                print("lat round minus : ", round(lat - 0.0002, 5))
                print('lon : ', lon)
                print("lon round plus : ", round(lon + 0.0002, 5))
                print('lon round minus : ', round(lon - 0.0002, 5))

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

                modbus_crc = str(msg[122:126])

                if Buoy.objects.filter(buoy_id=buoy_id):
                    Buoy.objects.filter(
                        buoy_id=buoy_id).update(battery=battery)

                    qs = Location.objects.filter(buoy__buoy_id=buoy_id, latitude__range=(
                        round(lat - 0.0002, 5), round(lat + 0.0002, 5)), longitude__range=(round(lon - 0.0002, 5), round(lon + 0.0002, 5)))

                    location = qs.first() if len(qs) == 1 else min(qs, key=lambda x: abs(
                        x.latitude - lat and x.longitude - lon)) if len(qs) > 1 else None

                    if location:
                        sensor1 = Sensor1.objects.create(
                            temperature=sensor1_temp,
                            oxygen_per=sensor1_oxy_per,
                            oxygen_mpl=sensor1_oxy_mpl,
                            oxygen_ppm=sensor1_oxy_ppm,
                        )
                        sensor2 = Sensor2.objects.create(
                            temperature=sensor2_temp,
                            ph=sensor2_ph,
                            redox=sensor2_redox,
                            ph_meter=sensor2_ph_meter,
                        )
                        sensor3 = Sensor3.objects.create(
                            temperature=sensor3_temp,
                            conductivity=sensor3_conduct,
                            salinity=sensor3_salt,
                            tds=sensor3_tds,
                        )
                        measure = Measure.objects.create(
                            location=location,
                            date=now.strftime('%Y-%m-%d'),
                            time=now.strftime('%H:%M:%S'),
                            sensor1=sensor1,
                            sensor2=sensor2,
                            sensor3=sensor3,
                            crc=modbus_crc,
                        )
                        sensor1, sensor2, sensor3.save()
                        measure.save()

                    # elif len(qs) > 1:
                    #     location = min(qs, key=lambda x: abs(x.latitude - lat and x.longitude - lon))

                    else:
                        buoy = Buoy.objects.get(buoy_id=buoy_id)
                        location = Location.objects.create(
                            buoy=buoy,
                            latitude=truncate(lat, 4),
                            longitude=truncate(lon, 4)
                        )
                        sensor1 = Sensor1.objects.create(
                            temperature=sensor1_temp,
                            oxygen_per=sensor1_oxy_per,
                            oxygen_mpl=sensor1_oxy_mpl,
                            oxygen_ppm=sensor1_oxy_ppm,
                        )
                        sensor2 = Sensor2.objects.create(
                            temperature=sensor2_temp,
                            ph=sensor2_ph,
                            redox=sensor2_redox,
                            ph_meter=sensor2_ph_meter,
                        )
                        sensor3 = Sensor3.objects.create(
                            temperature=sensor3_temp,
                            conductivity=sensor3_conduct,
                            salinity=sensor3_salt,
                            tds=sensor3_tds,
                        )
                        measure = Measure.objects.create(
                            location=location,
                            date=now.strftime('%Y-%m-%d'),
                            time=now.strftime('%H:%M:%S'),
                            sensor1=sensor1,
                            sensor2=sensor2,
                            sensor3=sensor3,
                            crc=modbus_crc,
                        )
                        location.save()
                        sensor1, sensor2, sensor3.save()
                        measure.save()
                else:
                    buoy = Buoy.objects.create(
                        buoy_id=int(msg[:8], 16),
                        battery=int(msg[8:10], 16)
                    )
                    location = Location.objects.create(
                        buoy=buoy,
                        latitude=truncate(lat, 4),
                        longitude=truncate(lon, 4)
                    )
                    sensor1 = Sensor1.objects.create(
                        temperature=sensor1_temp,
                        oxygen_per=sensor1_oxy_per,
                        oxygen_mpl=sensor1_oxy_mpl,
                        oxygen_ppm=sensor1_oxy_ppm,
                    )
                    sensor2 = Sensor2.objects.create(
                        temperature=sensor2_temp,
                        ph=sensor2_ph,
                        redox=sensor2_redox,
                        ph_meter=sensor2_ph_meter,
                    )
                    sensor3 = Sensor3.objects.create(
                        temperature=sensor3_temp,
                        conductivity=sensor3_conduct,
                        salinity=sensor3_salt,
                        tds=sensor3_tds,
                    )
                    measure = Measure.objects.create(
                        location=location,
                        date=now.strftime('%Y-%m-%d'),
                        time=now.strftime('%H:%M:%S'),
                        sensor1=sensor1,
                        sensor2=sensor2,
                        sensor3=sensor3,
                        crc=modbus_crc,
                    )
                    buoy.save()
                    location.save()
                    sensor1, sensor2, sensor3.save()
                    measure.save()

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
server_socket.bind(('172.31.11.52', 6557))
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
