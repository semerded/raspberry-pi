from gpiozero import LED, LightSensor
from time import sleep

AUTOROOD = LED(10)
AUTOGEEL = LED(9)
AUTOGROEN = LED(11)

FIETSROOD = LED(13)
FIETSGEEL = LED(19)
FIETSGROEN = LED(26)

LDR = LightSensor(21)

counter = 0

class stoplicht:
    def __init__(self, lichtRood, lichtGeel, lichtGroen) -> None:
        self.__lichtRood = lichtRood
        self.__lichtGeel = lichtGeel
        self.__lichtGroen = lichtGroen
        
        
    def Rood(self):
        self.__lichtRood.on()
        self.__lichtGeel.off()
        self.__lichtGroen.off()
        
    
    def Geel(self):
        self.__lichtRood.off()
        self.__lichtGeel.on()
        self.__lichtGroen.off()

        
    def Groen(self): 
        self.__lichtRood.off()
        self.__lichtGeel.off()
        self.__lichtGroen.on()       
    
fietsLicht = stoplicht(FIETSROOD, FIETSGEEL, FIETSGROEN)
autoLicht = stoplicht(AUTOROOD, AUTOGEEL, AUTOGROEN)


tijdGeel = 1
tijdGroen = 5
LDRactive = False
while True:
    
    
    if LDR.is_active:
        
        counter = 0
        fietsLicht.Geel()
        autoLicht.Geel()
        sleep(tijdGeel)
        fietsLicht.Groen()
        autoLicht.Rood()
        sleep(tijdGroen)
        fietsLicht.Geel()
        autoLicht.Geel()
        sleep(tijdGeel)
    else:
        autoLicht.Groen()
        fietsLicht.Rood()
       