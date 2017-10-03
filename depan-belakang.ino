#include <dht11.h>
#include <elapsedMillis.h>
#include "EmonLib.h"
#define interval 10000

elapsedMillis timer0;
dht11 DHT11;
EnergyMonitor emon1;

// Pin digital
const int PIN_DHT = 2;
const int PIN_PINTU = 4;
// Pin analog
const int PIN_SENSOR_GAS = A0;
const int PIN_ARUS = A1;

// default value
static int gas = 0;
static int suhu = 0;
static int kelembaban = 0;
static float arus = 0;


void setup() {
    timer0 = 0;
    emon1.current(PIN_ARUS, 30);
    pinMode(PIN_PINTU, INPUT_PULLUP);
    Serial.begin(9600);
}

void loop() {
    int pintu = digitalRead(PIN_PINTU);
    int chk = DHT11.read(PIN_DHT);
    kelembaban = (chk == 0) ? DHT11.humidity : 0;
    suhu = (chk == 0) ? DHT11.temperature : 0;

    int analogGas = analogRead(PIN_SENSOR_GAS);
    int gasNow = map(analogGas, 0, 1023, 0, 255);

    double Irms = emon1.calcIrms(1480);  // Calculate Irms only
    // daya = Irms*220.0;
    arus = Irms;

    if (gasNow > 0 || gasNow > gas) {
        gas = gasNow;
        timer0 = 0;
    }

    else if (gas > 0 && gasNow == 0 && timer0 < interval) {
        // jangan simpan variable gas yg baru
    }

    else {
        gas = gasNow;
        timer0 = 0;
    }


    delay(200);

    // Serial.print("Gas:");
    // Serial.println(gas);
    // Serial.print("Kelembaban:");
    // Serial.println(kelembaban);
    // Serial.print("Suhu:");
    // Serial.println(suhu);
    // Serial.print("Pintu:");
    // Serial.println(pintu);
    // Serial.print("Arus:");
    // Serial.println(arus);
    // Serial.println("------------------------------");

    boolean cmdOk = true;
    String cmd = "";

    while (Serial.available() != 0) {
        cmd = cmd + char(Serial.read());
        delay(20);
    }

    if (cmd.length() == 0) {
        return;
    }

    cmd.trim();
    cmd.toLowerCase();

    // UNTUK BACA GAS
    if (cmd == "gas") {
        Serial.println(gas);
    }

    // UNTUK BACA KELEMBABAN
    else if (cmd == "lembab") {
        Serial.println(kelembaban);
    }

    // UNTUK BACA SUHU
    else if (cmd == "suhu") {
        Serial.println(suhu);
    }

    // UNTUK BACA STATUS PINTU
    else if (cmd == "pintu") {
        Serial.println(pintu);
    }

    // UNTUK BACA STATUS PINTU
    else if (cmd == "arus") {
        Serial.println(arus);
    }

    // UNTUK BACA STATUS PINTU
    else if (cmd == "all") {
        Serial.print(suhu);
        Serial.print(",");
        Serial.print(kelembaban);
        Serial.print(",");
        Serial.print(gas);
        Serial.print(",");
        Serial.print(pintu);
        Serial.print(",");
        Serial.print(arus);
    }

    else {
        cmdOk = false;
    }

    if (!cmdOk) {
        Serial.println("---------------------------------------------");
        Serial.println("PERINTAH:");
        Serial.println("---------------------------------------------");
        Serial.println("gas \t\t: Membaca nilai gas");
        Serial.println("suhu \t\t: Membaca nilai suhu");
        Serial.println("lembab \t: Membaca nilai kelembaban");
        Serial.println("arus \t: Membaca nilai arus");
        Serial.println("pintu \t: Membaca status pintu");
    }
}
