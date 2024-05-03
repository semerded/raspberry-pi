import serial as Serial
import time

previousTime: int = 0
currentTime: int = time.time()
INTERVAL: int = 1

motorSpeed: int = 0

def getMotorSpeed(temperature, humidity):
    if temperature > 40:
        return 255
    elif temperature > 35:
        return 200
    elif temperature > 30:
        return 150
    elif temperature > 20:
        return 100
    elif temperature > 15:
        return 50
    else:
        return 0

if __name__ == '__main__':
    serial = Serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    serial.reset_input_buffer()

    while True:
        currentTime = time.time()

        if serial.in_waiting > 0:
            dhtValue = serial.readline().decode('utf-8').rstrip()
            
            try:
                temperature, humidity = dhtValue.split(";")
                motorSpeed = getMotorSpeed(int(temperature), int(humidity))
            except ValueError:
                continue

        if currentTime - previousTime >= INTERVAL:
            serial.write(str(f"{motorSpeed}\n").encode('ascii'))
            previousTime = currentTime
