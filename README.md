# iot-temperature-logger
 IoT Temperature & Humidity Logger (ESP32 + Python + SQLite)
 
##  Project Overview

This project reads Temperature & Humidity data from a DHT11 sensor using ESP32, sends it via Serial, and stores it in a SQLite database using Python (SQLAlchemy).

##  Project Structure
iot-temperature-logger/
│
├── esp32/
│   └── main.cpp          # ESP32 Arduino code
│
├── python/
│   └── app.py            # Python script (Serial → Database)
│
├── database/
│   └── iot_data.db       # Auto-created SQLite DB
│
├── platformio.ini
└── README.md

## Hardware Required
ESP32
DHT11 Sensor
Jumper wires

## Circuit Connections
DHT11 Pin	ESP32 Pin
VCC->	3.3V
GND	->GND
DATA	->GPIO 4

ESP32 Code (Arduino)
esp32/main.cpp

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
🐍 Python Code (Serial → Database)

📁 python/app.py

from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import serial

# Database setup
engine = create_engine('sqlite:///iot_data.db')
Base = declarative_base()

class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True)
    temperature = Column(Float)
    humidity = Column(Float)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Serial setup (Change COM port if needed)
ser = serial.Serial('COM10', 115200)

while True:
    try:
        line = ser.readline().decode(errors='ignore').strip()
        print("Raw:", line)

        if line == "ERROR":
            continue

        parts = line.split(',')

        if len(parts) == 2:
            temp = float(parts[0])
            hum = float(parts[1])

            data = SensorData(temperature=temp, humidity=hum)
            session.add(data)
            session.commit()

            print("Saved to DB ✔")
            print("----------------------")

    except Exception as e:
        print("Error:", e)
        
## requirements.txt
  sqlalchemy
  pyserial
  
## How to Run
## 1️ Upload Code to ESP32
Open in Arduino IDE / VS Code (PlatformIO)
Select board: ESP32
Upload main.cpp

## 2️ Install Python Dependencies
pip install -r requirements.txt

## 3️ Run Python Script
python app.py

## Output Example
Raw: 27.5,65.2
Saved to DB ✔

----------------------

## Database
File: iot_data.db
Table: sensor_data
id	temperature	humidity
1	27.5	65.2

## Future Improvements
Add LDR sensor
Build Flask API
Create Web Dashboard
Add real-time graphs

## Troubleshooting
## COM Port Error
Check correct port (COM10 / COM3 / etc.)
Close Arduino Serial Monitor

## Sensor ERROR
Check wiring
Ensure DHT library installed

## Author
Harsha G
