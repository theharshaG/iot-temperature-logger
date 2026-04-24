#include <Arduino.h>
#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(115200);
    dht.begin();
    delay(1000);
}

void loop() {
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();

    // Check sensor error
    if (isnan(temp) || isnan(hum)) {
        Serial.println("ERROR");
        delay(2000);
        return;
    }

    Serial.print(temp);
    Serial.print(",");
    Serial.println(hum);

    delay(2000);
}
