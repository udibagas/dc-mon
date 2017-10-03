import serial
import time
from threading import Thread
from pac import Pac
from sensor import Sensor
import requests

pac1 = Pac()
sensor_front = Sensor('/dev/arduino3')
sensor_rear = Sensor('/dev/arduino2')

def cek_all():
    try:
        data = sensor_front.get_all()
        print data
        suhu = int(data[0])
        kelembaban = int(data[1])
        gas = int(data[2])
        pintu = int(data[3])
        arus = float(data[4])
    except Exception as e:
        print "gagal"
        exit(0)

    # insert to database


    print "Gas : " + str(gas)

    if gas > 0:
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

    print "Suhu : " + str(suhu)
    print "Kelembaban : " + str(kelembaban)

    if suhu < 20:
        print "---------------------"
        print "suhu < 20 : compressor off"
        print "---------------------"
        pac1.set_compressor('off')

    if suhu > 24 or kelembaban < 40:
        print "--------------------------------------------------"
        print "suhu > 24 or kelembaban < 40: compressor on"
        print "--------------------------------------------------"
        pac1.set_compressor('on')

        if kelembaban > 60:
            print "----------------------------"
            print "kelembaban > 60 : heater on"
            print "----------------------------"
            pac1.set_heater('on')

    print "Pintu : " + str(pintu)

    if pintu:
        print "-----------------------"
        print "Pintu terbuka: LAMPU ON"
        print "-----------------------"
        pac1.set_lamp('on')

if __name__ == "__main__":
    # pac = Pac()
    # sensor_front = Sensor('/dev/ttyACM0')
    # sensor_rear = Sensor('/dev/serial_sensor_rear')

    try:
        while True:
            cek_all()
            time.sleep(1)

    except KeyboardInterrupt as e:
        print "Bye"
        pac1.turn_off()
        pac1.close_serial()
        sensor_front.close_serial()
        sensor_rear.close_serial()


    # untuk console
    # while True:
    #     try:
    #         dc      = DC()
    #         cmd     = raw_input("dc-controller>")
    #
    #         if cmd == "suhu":
    #             print str(dc.get_suhu())
    #
    #         elif cmd == "kelembaban":
    #             print str(dc.get_kelembaban())
    #
    #         elif cmd == "gas":
    #             print str(dc.get_gas())
    #
    #         elif cmd == "relay on":
    #             print str(dc.set_relay('on'))
    #
    #         elif cmd == "relay off":
    #             print str(dc.set_relay('off'))
    #
    #         elif cmd == "exit" or cmd == "quit":
    #             dc.close_serial()
    #             print("Bye");
    #             exit(0)
    #
    #         else:
    #             print "suhu \t kelembaban \t gas \t relay on \t relay off \t quit"
    #
    #     except KeyboardInterrupt:
    #         dc.close_serial()
    #         print("Bye");
    #         exit(0)
