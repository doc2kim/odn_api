import os
import sys
import json
import socket
import time
import threading


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

    from buoy.models import Buoy, Coordinate, MeasureTime, Measure
    now = time

    try:
        while True:
            receive_data = client_socket.recv(50)
            if not receive_data:
                print(addr, "to quit!")
                print("Waiting for next data...")
                break
            msg = receive_data.decode()
            if msg:
                print('Received from', addr, msg)
                if Buoy.objects.filter(id=int(msg[1:4])):
                    Buoy.objects.filter(id=int(msg[1:4])).update(
                        voltage=int(msg[4:7])/10)
                    if Coordinate.objects.filter(buoy_id__id=int(msg[1:4])):
                        coordinate = Coordinate.objects.filter(
                            buoy_id__id=int(msg[1:4]))
                        coordinate.update(
                            lat=int(msg[7:13])/10000, lon=int(msg[13:20])/10000)
                        measure_time = MeasureTime.objects.create(
                            coordinate=Coordinate.objects.get(
                                buoy_id__id=int(msg[1:4])),
                            date=now.strftime('%Y-%m-%d'),
                            time=now.strftime('%H:%M:%S')
                        )
                        measure = Measure.objects.create(
                            measure_time=measure_time,
                            temp=int(msg[20:24])/100,
                            oxy=int(msg[24:28])/100,
                            ph=int(msg[28:32])/100,
                            orp=int(msg[32:36]),
                            c4e=int(msg[36:40]),
                            ppt=int(msg[40:44])/100,
                            crc=str(msg[44:48]),
                        )
                        measure_time.save()
                        measure.save()
                    else:
                        buoy = Buoy.objects.get(id=int(msg[1:4]))
                        coordinate = Coordinate.objects.create(
                            buoy_id=buoy,
                            lat=int(msg[7:13])/10000,
                            lon=int(msg[13:20])/10000,
                        )
                        measure_time = MeasureTime.objects.create(
                            coordinate=coordinate,
                            date=now.strftime('%Y-%m-%d'),
                            time=now.strftime('%H:%M:%S')
                        )
                        measure = Measure.objects.create(
                            measure_time=measure_time,
                            temp=int(msg[20:24])/100,
                            oxy=int(msg[24:28])/100,
                            ph=int(msg[28:32])/100,
                            orp=int(msg[32:36]),
                            c4e=int(msg[36:40]),
                            ppt=int(msg[40:44])/100,
                            crc=str(msg[44:48]),
                        )
                        coordinate.save()
                        measure_time.save()
                        measure.save()
                else:
                    buoy = Buoy.objects.create(
                        id=int(msg[1:4]),
                        voltage=int(msg[4:7])/10
                    )
                    coordinate = Coordinate.objects.create(
                        buoy_id=buoy,
                        lat=int(msg[7:13])/10000,
                        lon=int(msg[13:20])/10000,
                    )
                    measure_time = MeasureTime.objects.create(
                        coordinate=coordinate,
                        date=now.strftime('%Y-%m-%d'),
                        time=now.strftime('%H:%M:%S')
                    )
                    measure = Measure.objects.create(
                        measure_time=measure_time,
                        temp=int(msg[20:24])/100,
                        oxy=int(msg[24:28])/100,
                        ph=int(msg[28:32])/100,
                        orp=int(msg[32:36]),
                        c4e=int(msg[36:40]),
                        ppt=int(msg[40:44])/100,
                        crc=str(msg[44:48]),
                    )
                    buoy.save()
                    coordinate.save()
                    measure_time.save()
                    measure.save()
                # print("id : ", int(msg[1:4]))
                # print("voltage : ", int(msg[4:7]))
                # print("lat : ", int(msg[7:13])/10000)
                # print("lon : ", int(msg[13:20])/10000)
                # print("temp : ",int(msg[20:24])/100 )
                # print("oxy : ", int(msg[24:28])/100)
                # print("ph : ", int(msg[28:32])/100)
                # print("orp : ", int(msg[32:36]))
                # print("c4e : ", int(msg[36:40]))
                # print("ppt : ", int(msg[40:44])/100)
                # print("crc : ", msg[44:48])
                # print("date : ", now.strftime('%Y-%m-%d'))
                # print("time : ", now.strftime('%H:%M:%S'))
                msg = "echo : " + msg
                echo_msg = msg.encode()

                # length = len(echo_msg);
                # client_socket.sendall(length.to_bytes(4, byteorder="big"));
                client_socket.sendall(echo_msg)
    except ConnectionResetError as e:
        print(e, addr)

    finally:
        client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('172.31.11.52', 6557))
server_socket.listen()

print('Server start up!')

try:
    while True:
        print('Receiving data...')
        client_socket, addr = server_socket.accept()
        th = threading.Thread(target=binder, args=(client_socket, addr))
        th.start()

except socket.error as e:
    print(e)


finally:
    server_socket.close()
