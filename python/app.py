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

# Serial setup
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

            print("Temperature:", temp) 
            print("Humidity:", hum) 
            print("----------------------")

            # Save to DB
            data = SensorData(temperature=temp, humidity=hum)
            session.add(data)
            session.commit()

            print("Saved to DB ✔")
            print("----------------------")

    except Exception as e:
        print("Error:", e)
