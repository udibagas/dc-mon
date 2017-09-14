import serial
import time
import random

class Pac:
    def __init__(self):
        self.my_serial = serial.Serial('/dev/ttyACM1', baudrate=9600, timeout=0)

        if not self.my_serial.is_open:
            print "DC controller not found!"
            exit(0)

        print "DC controller found"

    def set_compressor(self, set):
        self.my_serial.write('compressor ' + set)
        return self.my_serial.read(3)

    def set_fan(self, set):
        self.my_serial.write('fan ' + set)
        return self.my_serial.read()

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
        self.my_serial = serial.Serial(interface, baudrate=9600, timeout=0)

        if not self.my_serial.is_open:
            print "Sensor not found"
            exit(0)

        print "Sensor found"

    def get_suhu(self):
        self.my_serial.write('suhu')
        suhu = self.my_serial.readline()
        # suhu = random.uniform(19, 25)
        return suhu

    def get_kelembaban(self):
        self.my_serial.write('kelembaban')
        kelembaban = self.my_serial.readline()
        # kelembaban = random.uniform(39, 61)
        return kelembaban

    def get_gas(self):
        self.my_serial.write('gas')
        gas = self.my_serial.readline()
        # gas = random.uniform(20, 30)
        return gas

    def get_pintu(self):
        self.my_serial.write('pintu')
        pintu = self.my_serial.readline()
        # pintu = random.uniform(0,1)
        return gas

    def get_arus(self):
        # self.my_serial.write('arus')
        # gas = self.my_serial.readline()
        gas = random.uniform(0, 100)
        return gas

    def close_serial(self):
        self.my_serial.close()

if __name__ == "__main__":
    pac = Pac()
    sensor_front = Sensor('/dev/ttyACM2')
    # sensor_rear = Sensor('/dev/serial_sensor_rear')
    gas_counter = 0;

    while True:
        try:
            # DETEKSI ADA GAS ATAU TIDAK
            gas = sensor_front.get_gas()
            time.sleep(1)
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

            # DETEKSI SUHU & KELEMBABAN
            suhu = sensor_front.get_suhu()
            time.sleep(1)
            kelembaban = sensor_front.get_kelembaban()
            time.sleep(1)
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

            pintu = sensor_front.get_pintu()
            time.sleep(1)

            if pintu:
                pac.set_lamp('on')

            # time.sleep(5)

        except KeyboardInterrupt as e:
            print "Bye"
            pac.turn_off()
            pac.close_serial()
            sensor_front.close_serial()
            # sensor_rear.close_serial()

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
