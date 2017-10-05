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

void setup() {
    pinMode(PIN_COMPRESSOR, OUTPUT);
    pinMode(PIN_FAN, OUTPUT);
    pinMode(PIN_LAMPU, OUTPUT);
    pinMode(PIN_FIRE_ON, OUTPUT);
    pinMode(PIN_FIRE_OFF, OUTPUT);
    pinMode(PIN_HEATER, OUTPUT);
    pinMode(PIN_HI_PRESSURE, INPUT_PULLUP);

    // fan dan kompressor nyala di awal, makanya di comment
    // digitalWrite(PIN_FAN, HIGH);
    // digitalWrite(PIN_COMPRESSOR, HIGH);

    digitalWrite(PIN_LAMPU, HIGH);
    digitalWrite(PIN_HEATER, HIGH);
    digitalWrite(PIN_FIRE_ON, HIGH);
    digitalWrite(PIN_FIRE_OFF, HIGH);

    Serial.begin(9600);
}

void loop() {
    delay(300000) // durasi nyala
    digitalWrite(PIN_COMPRESSOR, HIGH);
    delay(180000) // durasi mati
    digitalWrite(PIN_COMPRESSOR, LOW);
}
