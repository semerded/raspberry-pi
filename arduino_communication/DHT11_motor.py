import serial as Serial, time
if __name__ == '__main__':
    serial = Serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    serial.reset_input_buffer()
    while True:
        if serial.in_waiting > 0:
            line = serial.readline().decode('utf-8').rstrip()
            print(line)