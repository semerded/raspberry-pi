import I2C_LDC as I2C_LDC
import busio, board, digitalio, adafruit_lis3dh
from time import sleep

lcd = I2C_LDC.lcd()
I2C = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D24)
sensor = adafruit_lis3dh.LIS3DH_I2C(I2C, address=25, int1 = int1)

lcd.lcd_display_string("hello world!")

while True:
    x, y, z = sensor.acceleration
    print(x, y, z)
    sleep(0.2)


sleep(1)

lcd.lcd_clear()