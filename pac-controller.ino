#include <elapsedMillis.h>

elapsedMillis timer0;
#define interval 300000

// WARNING !!!
// HIGH -> default relay 2 channel

// OUTPUT
const int PIN_COMPRESSOR = 2;
const int PIN_FAN = 4;
const int PIN_LAMPU = 7;
const int PIN_HEATER = 8;
const int PIN_FIRE_ON = 12;
const int PIN_FIRE_OFF = 13;

// INPUT
const int PIN_HI_PRESSURE = 9;
int nyala = 1;

void setup() {
    timer0 = 0;

    pinMode(PIN_COMPRESSOR, OUTPUT);
    pinMode(PIN_FAN, OUTPUT);
    pinMode(PIN_LAMPU, OUTPUT);
    pinMode(PIN_FIRE_ON, OUTPUT);
    pinMode(PIN_FIRE_OFF, OUTPUT);
    pinMode(PIN_HEATER, OUTPUT);
    pinMode(PIN_HI_PRESSURE, INPUT_PULLUP);

    // default matikan dulu semua
    digitalWrite(PIN_FAN, HIGH);
    digitalWrite(PIN_COMPRESSOR, HIGH);
    digitalWrite(PIN_LAMPU, HIGH);
    digitalWrite(PIN_HEATER, HIGH);
    digitalWrite(PIN_FIRE_ON, HIGH);
    digitalWrite(PIN_FIRE_OFF, HIGH);

    Serial.begin(9600);
}

void loop() {
    // if (timer0 > interval) {
    //     timer0 -= interval;
    //     nyala = !nyala;
    //     digitalWrite(PIN_COMPRESSOR, !nyala)
    // }

    boolean cmdOk = true;
    String cmd = "";

    // detect high pressure
    int hiPressure = digitalRead(PIN_HI_PRESSURE);
    if (hiPressure == LOW) {
        digitalWrite(PIN_FAN, HIGH);
        digitalWrite(PIN_COMPRESSOR, HIGH);
        digitalWrite(PIN_HEATER, HIGH);
    }

    while (Serial.available() != 0) {
        cmd = cmd + char(Serial.read());
        delay(20);
    }

    if (cmd.length() == 0) {
        return;
    }

    cmd.trim();
    cmd.toLowerCase();

    if (cmd == "compressor on") {
        digitalWrite(PIN_COMPRESSOR, LOW);
        Serial.println("OK");
    }

    else if (cmd == "compressor off") {
        digitalWrite(PIN_COMPRESSOR, HIGH);
        Serial.println("OK");
    }

    else if (cmd == "fan on") {
        digitalWrite(PIN_FAN, LOW);
        Serial.println("OK");
    }

    else if (cmd == "fan off") {
        digitalWrite(PIN_FAN, HIGH);
        Serial.println("OK");
    }

    else if (cmd == "lamp on") {
        digitalWrite(PIN_LAMPU, LOW);
        Serial.println("OK");
    }

    else if (cmd == "lamp off") {
        digitalWrite(PIN_LAMPU, HIGH);
        Serial.println("OK");
    }

    // buka katup cukup 5 detik
    else if (cmd == "fire on") {
        digitalWrite(PIN_FIRE_ON, LOW);
        delay(5000);
        digitalWrite(PIN_FIRE_ON, HIGH);
        Serial.println("OK");
    }

    // tutup katup cukup 5 detik
    else if (cmd == "fire off") {
        digitalWrite(PIN_FIRE_OFF, LOW);
        delay(5000);
        digitalWrite(PIN_FIRE_OFF, HIGH);
        Serial.println("OK");
    }

    else if (cmd == "heater on") {
        digitalWrite(PIN_HEATER, LOW);
        Serial.println("OK");
    }

    else if (cmd == "heater off") {
        digitalWrite(PIN_HEATER, HIGH);
        Serial.println("OK");
    }

    else if (cmd == "pac off") {
        digitalWrite(PIN_COMPRESSOR, HIGH);
        digitalWrite(PIN_FAN, HIGH);
        digitalWrite(PIN_HEATER, HIGH);
        Serial.println("OK");
    }

    else if (cmd == "highpress status") {
        Serial.println(hiPressure);
    }

    else {
        cmdOk = false;
    }

    if (!cmdOk) {
        Serial.println("compressor on/off \t fan on/off \f lamp on/off \t fire on/off \t heater on/off");
    }
}
