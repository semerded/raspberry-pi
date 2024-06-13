import serial as Serial
import time

previousTime: float = 0
currentTime: float = time.time()
INTERVAL: int = 1


if __name__ == "__main__":
    serial = Serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    serial.reset_input_buffer()
    
    while True:
        currentTime = time.time()
        
        if serial.in_waiting > 0:
            value = serial.readline().decode('utf-8').rstrip()
            
        
        if currentTime - previousTime >= INTERVAL:
            serial.write(str(f"{value}\n").encode('ascii')) 
            previousTime = currentTime