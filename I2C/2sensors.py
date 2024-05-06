import time, board, adafruit_bh1750, smbus2, bme280, I2C_LDC

# bme280
port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

# lcd
lcd = I2C_LDC.lcd()

# bh1750
i2c = board.I2C()
sensor = adafruit_bh1750.BH1750(i2c)

while True:
    bme280data = bme280.sample(bus, address, calibration_params)
    temperature = bme280data.temperature
    pressure = bme280data.pressure
    humidity = bme280data.humidity
    
    lightLevel = sensor.lux
    
    lcd.lcd_display_string(f"{round(temperature, 2)}°C|{round(humidity)}%")
    lcd.lcd_display_string(f"{round(pressure, 2)}hPa|{round(lightLevel, 2)}Lux")
    
    
    time.sleep(1)