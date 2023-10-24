"""
volkomen rood stoplicht
gemaakt door Sem Van Broekhoven
copyright © 2023
------------------------------------------------------------
Op een 'volkomen rood kruispunt' staan 's avonds alle of sommige
verkeerslichten op rood. Zodra er uit een bepaalde richting verkeer
aankomt, springt aan die kant het licht op groen. Zo'n schakeling
bouw je in het klein na: een doorgaande autoweg en een
fietsersoversteekplaats. Overdag gaan de verkeerslichten op de
autoweg elke twee minuten op rood.De verkeerslichten op de
fietsersoversteekplaats staan dan 20 seconden lang op groen. 's
Avonds zijn de verkeerslichten op de autoweg altijd groen, totdat er
een fietser aankomt.De fietser wordt gedetecteerd doordat het licht
van zijn fietslamp op een LDR valt; ook de daglichtsituatie wordt door
deze LDR gedetecteerd. Ga uit van één fietser en één auto.De
fietser heeft een LED koplamp, die ook brandt bij stilstand
------------------------------------------------------------
alleen voor eigen gebruik - geen commerciele doeleinde
check zeker deze site https://eelslap.com/ 
groetjes
Sem
6IICT
"""
# witregel om de code makkelijker leesbaar te maken
# start van de code
from gpiozero import LED, LightSensor # import de componenten uit de library die je nodig hebt
from time import sleep # om delay's toe te voegen
# witregel om de code makkelijker leesbaar te maken
AUTOROOD = LED(10) # duid de led aan op pin 10
AUTOGEEL = LED(9) # duid de led aan op pin 9
AUTOGROEN = LED(11) # duid de led aan op pin 11
# witregel om de code makkelijker leesbaar te maken
FIETSROOD = LED(13) # duid de led aan op pin 13
FIETSGEEL = LED(19) # duid de led aan op pin 19
FIETSGROEN = LED(26) # duid de led aan op pin 26
# witregel om de code makkelijker leesbaar te maken
LDR = LightSensor(21) # zet de LDR op pin 21
# witregel om de code makkelijker leesbaar te maken
class stoplicht: # maak een class aan met de verschillende standen van het stoplicht
    def __init__(self, lichtRood, lichtGeel, lichtGroen) -> None: # maak de class aan en voeg de verschillende lichten toe
        self.__lichtRood = lichtRood # zet de functie van de class gelijk aan de ingegeven waarde
        self.__lichtGeel = lichtGeel # zet de functie van de class gelijk aan de ingegeven waarde
        self.__lichtGroen = lichtGroen # zet de functie van de class gelijk aan de ingegeven waarde
# witregel om de code makkelijker leesbaar te maken
# witregel om de code makkelijker leesbaar te maken    
    def Rood(self): # lichtstand rood
        self.__lichtRood.on() # zet lamp aan
        self.__lichtGeel.off() # zet lamp uit
        self.__lichtGroen.off() # zet lamp uit
# witregel om de code makkelijker leesbaar te maken    
# witregel om de code makkelijker leesbaar te maken   
    def Geel(self): # lichtstand geel
        self.__lichtRood.off() # zet lamp uit
        self.__lichtGeel.on() # zet lamp aan
        self.__lichtGroen.off() # zet lamp uit
# witregel om de code makkelijker leesbaar te maken
# witregel om de code makkelijker leesbaar te maken       
    def Groen(self): # lichtstand groen
        self.__lichtRood.off() # zet lamp uit
        self.__lichtGeel.off() # zet lamp uit
        self.__lichtGroen.on() # zet lamp aan     
# witregel om de code makkelijker leesbaar te maken
fietsLicht = stoplicht(FIETSROOD, FIETSGEEL, FIETSGROEN) # voeg de standen van de class aan de fietslichten toe
autoLicht = stoplicht(AUTOROOD, AUTOGEEL, AUTOGROEN) # voeg de standen van de class aan de autolichten toe
# witregel om de code makkelijker leesbaar te maken
tijdGeel = 1 # de tijd dat het geel is
tijdGroen = 5 # de tijd dat het groen/rood is
wachtTotDeDoorHetGeelRijdersVoorbijZijn = 1 # tijd tussen dat het ene licht op rood springt en het ander op groen
# witregel om de code makkelijker leesbaar te maken
# bij het starten van het programma staan de lichten op rood 
fietsLicht.Rood() # zet fietslicht op rood
autoLicht.Rood() # zet autolicht op rood
sleep(tijdGroen) # tijd dat het licht rood blijft
# witregel om de code makkelijker leesbaar te maken
while True: # de loop die zich zal blijven herhalen
    if LDR.is_active: # als de LDR licht detecteerd
        fietsLicht.Rood() # rood licht voor fietsers
        sleep(wachtTotDeDoorHetGeelRijdersVoorbijZijn) # wachtTotDeDoorHetGeelRijdersVoorbijZijn
        autoLicht.Groen() # groen licht voor auto's
        sleep(tijdGroen) # tijd dat het groen/rood blijft
        autoLicht.Geel() # geel licht voor auto's
        sleep(tijdGeel) # tijd dat het geel blijft
        autoLicht.Rood() # rood licht voor auto's
        sleep(wachtTotDeDoorHetGeelRijdersVoorbijZijn) # wachtTotDeDoorHetGeelRijdersVoorbijZijn
        fietsLicht.Groen() # groen licht voor fietsers
        sleep(tijdGroen) # tijd dat het groen/rood blijft
        fietsLicht.Geel() # geel licht voor fietsers
        sleep(tijdGeel) # tijd dat het geel blijft
    else: # als het donker is
        autoLicht.Groen() # autolicht blijft op groen staan
        fietsLicht.Rood() # fietslicht blijft op rood staan