import serial
import time
# import random
import MySQLdb
from threading import Thread

class Pac:
    def __init__(self):
        try:
            self.my_serial = serial.Serial('/dev/arduino1', baudrate=9600, timeout=1)
            # print "DC controller found"
        except Exception as e:
            print "DC controller not found!"
            exit(0)

    def set_compressor(self, set):
        self.my_serial.write('compressor ' + set)
        return self.my_serial.readline()

    def set_fan(self, set):
        self.my_serial.write('fan ' + set)
        return self.my_serial.readline()

    def set_fire(self, set):
        self.my_serial.write('fire ' + set)
        return self.my_serial.readline()

    def set_heater(self, set):
        self.my_serial.write('heater ' + set)
        return self.my_serial.readline()

    def set_lamp(self, set):
        self.my_serial.write('lamp ' + set)
        return self.my_serial.readline()

    def turn_off(self):
        self.my_serial.write('pac off')
        return self.my_serial.readline()

    def close_serial(self):
        self.my_serial.close()
        return self.my_serial.readline()

class Sensor:
    def __init__(self, interface):
        try:
            self.my_serial = serial.Serial(interface, baudrate=9600, timeout=1)
            # print "Sensor found"
        except Exception as e:
            print "Sensor not found"
            exit(0)

    def get_suhu(self):
        self.my_serial.write('suhu')
        suhu = self.my_serial.readline()
        # suhu = random.uniform(19, 25)
        return int(suhu)

    def get_kelembaban(self):
        self.my_serial.write('lembab')
        kelembaban = self.my_serial.readline()
        return int(kelembaban)

    def get_gas(self):
        self.my_serial.write('gas')
        gas = self.my_serial.readline()
        return int(gas)

    def get_pintu(self):
        self.my_serial.write('pintu')
        pintu = self.my_serial.readline()
        return int(pintu)

    def get_arus(self):
        self.my_serial.write('arus')
        arus = self.my_serial.readline()
        return float(arus)

    def get_all(self):
        self.my_serial.write('all')
        data = self.my_serial.readline()
        # suhu, lembab, gas, pintu, arus
        return data.split(",")

    def close_serial(self):
        self.my_serial.close()

pac = Pac()
sensor_front = Sensor('/dev/arduino3')
sensor_rear = Sensor('/dev/arduino2')

def cek_all():
    try:
        data = sensor_front.get_all()
        print data
        # suhu = int(data[0])
        # kelembaban = int(data[1])
        # gas = int(data[2])
        # pintu = int(data[3])
        # arus = float(data[4])
    except Exception as e:
        print "gagal"

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
            pac.turn_off()
            # hidupkan fire suppression selama 5 detik
            print "fire suppression on"
            print "----------------------"
            pac.set_fire('on')
            time.sleep(20)
            pac.set_fire('off')

    print "Suhu : " + str(suhu)
    print "Kelembaban : " + str(kelembaban)

    if suhu < 20:
        print "---------------------"
        print "suhu < 20 : compressor off"
        print "---------------------"
        pac.set_compressor('off')

    if suhu > 24 or kelembaban < 40:
        print "--------------------------------------------------"
        print "suhu > 24 or kelembaban < 40: compressor on"
        print "--------------------------------------------------"
        pac.set_compressor('on')

        if kelembaban > 60:
            print "----------------------------"
            print "kelembaban > 60 : heater on"
            print "----------------------------"
            pac.set_heater('on')

    print "Pintu : " + str(pintu)

    if pintu:
        print "-----------------------"
        print "Pintu terbuka: LAMPU ON"
        print "-----------------------"
        pac.set_lamp('on')

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
        pac.turn_off()
        pac.close_serial()
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
