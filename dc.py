import time
from threading import Thread
from pac import Pac
from sensor import Sensor
import requests
import sys

def cek_all():
    global gas_counter
    global suhu_depan
    global lembab_depan
    global gas_depan
    global suhu_belakang
    global lembab_belakang
    global gas_belakang
    global data_depan_ok
    global data_belakang_ok

    try:
        data_depan = sensor_depan.get_all()
        data_depan_ok = True
        suhu_depan = int(data_depan[0])
        lembab_depan = int(data_depan[1])
        gas_depan = int(data_depan[2])
        pintu_depan = int(data_depan[3])
        arus_input_ets = float(data_depan[4])
        print data_depan

    except Exception as e:
        print "GAGAL MEMBACA SENSOR DEPAN"

    # insert to database (local & unitron)
    if data_depan_ok:
        try:
            # TODO: update nilai parameter
            r0 = requests.get('http://localhost/api/log?sensor_id=')
            r1 = requests.get('http://10.45.5.20/smading/api/log?sensor_id=')
            # TODO: update status pintu

        except Exception as e:
            pass

    try:
        data_belakang = sensor_belakang.get_all()
        data_belakang_ok = True
        suhu_belakang = int(data_belakang[0])
        lembab_belakang = int(data_belakang[1])
        gas_belakang = int(data_belakang[2])
        pintu_belakang = int(data_belakang[3])
        arus_input_ups = float(data_belakang[4])
        print data_belakang

    except Exception as e:
        print "GAGAL MEMBACA SENSOR BELAKANG"

    if data_belakang_ok:
        # insert to database (local & unitron)
        try:
            r0 = requests.get('http://localhost/api/log?sensor_id=')
            r1 = requests.get('http://10.45.5.20/smading/api/log?sensor_id=')
            # TODO: update status pintu
        except Exception as e:
            pass

    if data_depan_ok or data_belakang_ok:
        # paling urgent cek gas dulu
        if cek_gas and (gas_depan > kalibrasi_gas_depan or gas_belakang > kalibrasi_gas_belakang):
            # increase counter
            gas_counter += 1

            if gas_counter == 3:
                # reset counter
                gas_counter = 0
                # matikan ac dulu
                print "----------------------"
                print "gas detected. pac off"
                pac1.turn_off()
                # hidupkan fire suppression selama 5 detik
                print "fire suppression on"
                print "----------------------"
                pac1.set_fire('on')
                time.sleep(20)
                pac1.set_fire('off')

        # if suhu_depan < 20 or suhu_belakang < 20:
        if suhu_depan < 20:
            pac1.set_compressor('off')

        # if suhu_depan > 24 or lembab_depan < 40 or suhu_belakang > 28 or lembab_belakang < 40:
        if suhu_depan > 24:
            pac1.set_compressor('on')

            # if lembab_depan > 60 or lembab_belakang > 60:
            #     pac1.set_heater('on')


pac1 = Pac()
sensor_depan = Sensor('/dev/arduino3')
sensor_belakang = Sensor('/dev/arduino2')
kalibrasi_gas_depan = 90
kalibrasi_gas_belakang = 90
gas_counter = 0
cek_gas = False
suhu_depan = 0
lembab_depan = 0
gas_depan = 0
suhu_belakang = 0
lembab_belakang = 0
gas_belakang = 0
data_depan_ok = False
data_belakang_ok = False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        pac1.set_fan("on")
        time.sleep(3)

        try:
            while True:
                cek_all()
                time.sleep(5)

        except KeyboardInterrupt as e:
            print "Bye"
            pac1.turn_off()
            pac1.close_serial()
            sensor_depan.close_serial()
            sensor_belakang.close_serial()

    # untuk console
    while True:
        try:
            cmd = raw_input("dc-controller> ")

            if cmd == "suhu depan":
                print str(sensor_depan.get_suhu())

            elif cmd == "lembab depan":
                print str(sensor_depan.get_lembab())

            elif cmd == "gas depan":
                print str(sensor_depan.get_gas())

            elif cmd == "arus depan":
                print str(sensor_depan.get_arus())

            elif cmd == "pintu depan":
                print str(sensor_depan.get_pintu())

            elif cmd == "all depan":
                print str(sensor_depan.get_all())

            elif cmd == "suhu belakang":
                print str(sensor_belakang.get_suhu())

            elif cmd == "lembab belakang":
                print str(sensor_belakang.get_lembab())

            elif cmd == "gas belakang":
                print str(sensor_belakang.get_gas())

            elif cmd == "arus belakang":
                print str(sensor_belakang.get_arus())

            elif cmd == "pintu belakang":
                print str(sensor_belakang.get_pintu())

            elif cmd == "all belakang":
                print str(sensor_belakang.get_all())

            elif cmd == "set fan on":
                print str(pac1.set_fan("on"))

            elif cmd == "set fan off":
                print str(pac1.set_fan("off"))

            elif cmd == "set compressor on":
                print str(pac1.set_compressor("on"))

            elif cmd == "set compressor off":
                print str(pac1.set_compressor("off"))

            elif cmd == "set heater on":
                print str(pac1.set_heater("on"))

            elif cmd == "set heater off":
                print str(pac1.set_heater("off"))

            elif cmd == "set lamp on":
                print str(pac1.set_lamp("on"))

            elif cmd == "set lamp off":
                print str(pac1.set_lamp("off"))

            elif cmd == "set fire on":
                print str(pac1.set_fire("on"))

            elif cmd == "set fire off":
                print str(pac1.set_fire("off"))

            elif cmd == "highpress status":
                print str(pac1.highpress_status())

            elif cmd == "pac off":
                print str(pac1.turn_off())

            elif cmd == "exit" or cmd == "quit":
                sensor_depan.close_serial()
                sensor_belakang.close_serial()
                pac1.close_serial()
                print("Bye");
                exit(0)

            else:
                print "suhu depan/belakang"
                print "lembab depan/belakang"
                print "gas depan/belakang"
                print "arus depan/belakang"
                print "pintu depan/belakang"

        except KeyboardInterrupt:
            sensor_depan.close_serial()
            sensor_belakang.close_serial()
            pac1.close_serial()
            print("Bye");
            exit(0)
