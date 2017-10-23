import time
from threading import Thread
from pac import Pac
from sensor import Sensor
import requests
import sys
import logging
import logging.handlers
import os.path
import json

def cek_all():
    global gas_counter
    global suhu_depan
    global suhu_belakang
    global lembab_depan
    global lembab_belakang
    global gas_depan
    global gas_belakang
    global pintu_depan
    global pintu_belakang
    global data_depan_ok
    global data_belakang_ok
    global compressor_on
    global fan_on

    if compressor_on:
        compressor_status = "ON"
    else:
        compressor_status = "OFF"

    try:
        data_depan = sensor_depan.get_all()
        data_depan_ok = True
        suhu_depan = int(data_depan[0])
        lembab_depan = int(data_depan[1])
        gas_depan = int(data_depan[2])
        pintu_depan = int(data_depan[3])
        arus_input_ets = float(data_depan[4])

        logger.info(
            "[DPN] suhu:" + str(suhu_depan)
            + ", lembab:" + str(lembab_depan)
            + ", gas:" + str(gas_depan)
            + ", pintu:" + str(pintu_depan)
            + ", arus:" + str(arus_input_ets)
            + ", compressor: " + compressor_status
        )

    except Exception as e:
        logger.error("Gagal membaca sensor depan")

    try:
        data_belakang = sensor_belakang.get_all()
        data_belakang_ok = True
        suhu_belakang = int(data_belakang[0])
        lembab_belakang = int(data_belakang[1])
        gas_belakang = int(data_belakang[2])
        pintu_belakang = int(data_belakang[3])
        arus_input_ups = float(data_belakang[4])

        logger.info(
            "[BLK] suhu:" + str(suhu_belakang)
            + ", lembab:" + str(lembab_belakang)
            + ", gas:" + str(gas_belakang)
            + ", pintu:" + str(pintu_belakang)
            + ", arus:" + str(arus_input_ups)
            + ", compressor: " + compressor_status
        )

    except Exception as e:
        logger.error("Gagal membaca sensor belakang")

    data = {
        "suhu_depan" : suhu_depan,
        "suhu_belakang" : suhu_belakang,
        "lembab_depan" : lembab_depan,
        "lembab_belakang" : lembab_belakang,
        "gas_depan" : gas_depan,
        "gas_belakang" : gas_belakang,
        "pintu_depan" : pintu_depan,
        "pintu_belakang" : pintu_belakang,
        "arus_input_ets" : arus_input_ets,
        "arus_input_ups" : arus_input_ups,
        "fan": fan_on,
        "compressor": compressor_on
    }

    try:
        r = requests.post(config["api_url"] + "sensorLog", data=data)
    except Exception as e:
        logger.info("save to db failed" + str(e))

    if r.status_code == requests.codes.ok:
        logger.info("save to db success")
    else:
        logger.info("save to db failed")

    if data_depan_ok or data_belakang_ok:
        if cek_gas and (gas_depan > kalibrasi_gas_depan or gas_belakang > kalibrasi_gas_belakang):
            gas_counter += 1

            if gas_counter == 3:
                gas_counter = 0
                logger.info("Gas terdeteksi!!!")
                logger.info("PAC OFF")
                pac1.turn_off()
                logger.info("Fire suppression ON")
                pac1.set_fire('on')
                time.sleep(20)
                logger.info("Fire suppression OFF")
                pac1.set_fire('off')

        if suhu_depan < config["min_value"]["suhu_depan"]:
            if compressor_on:
                compressor_on = False
                logger.info("SUHU DEPAN < " + str(config["min_value"]["suhu_depan"]) + ". COMPRESSOR OFF")
                pac1.set_compressor('off')

        # if suhu_depan > 24 or lembab_depan < 40 or suhu_belakang > 28 or lembab_belakang < 40:
        if suhu_depan > config["max_value"]["suhu_depan"]:
            if not compressor_on:
                compressor_on = True
                logger.info("SUHU DEPAN > " + str(config["max_value"]["suhu_depan"]) + ". COMPRESSOR ON")
                pac1.set_compressor('on')

            # if lembab_depan > 60 or lembab_belakang > 60:
            #     pac1.set_heater('on')

if __name__ == "__main__":
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
    log_file_path = os.path.join(os.path.dirname(__file__), 'dc.log')

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=1024000, backupCount=100)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    try:
        logger.debug("Reading config file...")
        with open(config_file_path) as config_file:
            config = json.load(config_file)
    except Exception as e:
        logger.error("Gagal membuka file konfigurasi (config.json)")
        exit()

    try:
        logger.debug("Inisiasi PAC controller...")
        pac1 = Pac()
        logger.info("PAC Controller OK!")
    except Exception as e:
        logger.info("PAC Controller tidak ditemukan!")

    try:
        logger.debug("Inisiasi Sensor depan...")
        sensor_depan = Sensor(config["device"]["sensor_depan"])
        logger.info("Sensor depan OK!")
    except Exception as e:
        logger.info("Sensor depan tidak ditemukan!")

    try:
        logger.debug("Inisiasi Sensor belakang...")
        sensor_belakang = Sensor(config["device"]["sensor_belakang"])
        logger.info("Sensor belakang OK!")
    except Exception as e:
        logger.info("Sensor belakang tidak ditemukan!")

    kalibrasi_gas_depan = 90
    kalibrasi_gas_belakang = 90
    gas_counter = 0
    cek_gas = False
    suhu_depan = 0
    suhu_belakang = 0
    lembab_depan = 0
    lembab_belakang = 0
    gas_depan = 0
    gas_belakang = 0
    pintu_depan = 1
    pintu_belakang = 1
    data_depan_ok = False
    data_belakang_ok = False
    fan_on = False
    compressor_on = False

    if len(sys.argv) > 1 and sys.argv[1] == "run":
        logger.debug("Tunda biar serial siap dulu...")
        time.sleep(3)
        logger.debug("Menghidupkan fan...")
        fan = pac1.set_fan("on")
        logger.debug("FAN status : " + str(fan))
        fan_on = True
        logger.debug("Checking environment...")
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
