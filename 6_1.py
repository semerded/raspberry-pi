from gpiozero import LightSensor

LDR = LightSensor(18)

while True:
    print(LDR.value)
    LDR.wait_for_active()
    print('I see the light')
    LDR.wait_for_inactive()
    print("Het is donker in huis")
    