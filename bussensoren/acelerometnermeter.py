import smbus, time

sensorAdress = 0x19
lcdAdress = 0x27

bus = smbus.SMBus(1)

def bearing255():
    return bus.read_byte_data(sensorAdress, 1)

def bearing3599():
    bear1 = bus.read_byte_data(sensorAdress, 2)
    bear2 = bus.read_byte_data(sensorAdress, 3)
    bear = (bear1 << 8) + bear2
    return bear/10.0

while True:
    print(bearing3599())
    print(bearing255())
    time.sleep(1)
    