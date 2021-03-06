import serial

class Pac:
    def __init__(self):
        try:
            self.my_serial = serial.Serial('/dev/arduino1', baudrate=9600, timeout=1)
        except Exception as e:
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

    def highpress_status(self):
        self.my_serial.write('highpress status')
        return self.my_serial.readline()

    def turn_off(self):
        self.my_serial.write('pac off')
        return self.my_serial.readline()

    def close_serial(self):
        self.my_serial.close()
