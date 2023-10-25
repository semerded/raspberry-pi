import gpiozero as io
from time import time, ctime
from os.path import isfile
import Adafruit_DHT # library om de DHT11 uit te lezen

BUTTON = io.Button(11) # sluit knop aan op pin 11

FILELOCATION = "DHT11log.txt" # bestandslocatie voor het log bestand

# maak vars aan
writeData = False
previousTime = 0
timeBetweenLog = 5 # tijd in seconden tussen elke log

"""
ik durf te wedden dat niemand dit heeft toegevoegd
ik heb dit gedaan om het u wat gemakkelijker te maken
(pluspuntjes?)
"""
if isfile(FILELOCATION) is False: # maakt het log bestand aan als deze nog niet bestaat
    file = open(FILELOCATION, "w")
    file.close()
    del file # schoon var naam op
    
def stateChangeDetection():
    global writeData, previousTime, currentTime # waardes die aangepast worden worden global gemaakt
    writeData = not writeData # geeft de boolean de tegenovergestelde waarde --> true wordt false en false wordt true
    previousTime = currentTime # zet de vorige tijd gelijk aan de huidige tijd (wachttijd voor log wordt terug 5 seconden)
    if writeData: # print info in terminal
        print("data logging started")
    else:
        print("data logging stopped")

print("-- program started --")
while True: # main loop
    currentTime = time() # sla huidige tijd op in var
    
    BUTTON.when_activated = stateChangeDetection # voer functie uit als de knop wordt ingedrukt
    
    if writeData: # als er data geschereven mag worden
        vochtigheid, temperatuur = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4, 2) # lees de data van de DHT11 uit (2 staat voor hoevaak hij de data opnieuw zal proberen uit te lezen als er iets fout mocht gaan)
        if currentTime - previousTime > timeBetweenLog: # als de verlopen tijd groter dan 5 seconden is wordt de data gelogged
            if vochtigheid != None and temperatuur != None: # als de data succesvol uitgelezen wordt
                # open de logfile om de data naar toe te schrijven (de data wordt achter de oude data toegevoegd)
                with open(FILELOCATION, "a") as saveFile:
                    logTime = ctime() # lees de huidige tijd uit om te loggen in het bestand en in de terminal
                    print("data loged at %s" % logTime)
                    saveFile.write(f"{logTime} | temperature: {temperatuur}°C | humidity: {vochtigheid}%\n")
                previousTime = currentTime # stel de vorige tijd gelijk met de huidige tijd zodat er weer 5 seconden gewacht moet worden
            else: # als de data niet is uitgelezen 
                print("failed to read sensor")
                # de vorige tijd wordt niet gelijk gesteld aan de huidige tijd zodat het programma niet terug 5 seconden hoeft te wachten om data te schrijven