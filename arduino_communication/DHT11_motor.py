import serial as Serial, time

perviousTime: int
currentTime: int = time.time()
INTERVAL: int = 1000

motorSpeed = 0

if __name__ == '__main__':
    serial = Serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    serial.reset_input_buffer()
    
    while True:
        currentTime = time.time()
        
        if serial.in_waiting > 0:
            dhtValue = serial.readline().decode('utf-8').rstrip()
            print(dhtValue)
            
            try:
                dhtValue = int(dhtValue)
            except ValueError:
                continue
        
        if currentTime - perviousTime >= INTERVAL:
            Serial.write(b"%s\n" %motorSpeed)
            