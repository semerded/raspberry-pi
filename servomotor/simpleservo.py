from gpiozero import AngularServo
from time import sleep

servo = AngularServo(17)

servo.angle = 90
sleep(1)
servo.angle = 0
sleep(1)
servo.angle = -90
sleep(1)
servo.angle = -45
sleep(1)
servo.angle = 45
