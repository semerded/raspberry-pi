import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

while True:
    GPIO.output(12, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(12, GPIO.LOW)
    time.sleep(1)