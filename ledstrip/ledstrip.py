from rpi_ws281x import *
from time import sleep

LED_COUNT = 95
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_INVERT = False
LED_DMA = 10
LED_BRIGHTNESS = 65
LED_CHANNEL = 0
ledStrip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

class LedStripControl:
    def __init__(self, ledStrip: Adafruit_NeoPixel) -> None:
        self.strip = ledStrip
        
        
    def setColor(self, color):
        for index in range(self.strip.numPixels()):
            self.strip.setPixelColor(index, Color(*color))
        self.strip.show()
        
    def clear(self):
        self.setColor((0, 0, 0))

    def colorSnake(self, color, snakeLength: int, timeInMsec: int):
        for index in range(self.strip.numPixels()):
            self.strip.setPixelColor(index, Color(*color))
            
            if index > snakeLength:
                self.strip.setPixelColor(index - snakeLength, Color(*0, 0, 0))
                
            self.strip.show()
            sleep(timeInMsec / self.strip.numPixels())
            
        
    def colorLineProgress(self, color, timeInMsec: int):
        for index in range(self.strip.numPixels()):
            self.strip.setPixelColor(index, Color(*color))
            self.strip.show()
            sleep(timeInMsec / self.strip.numPixels())
        
        
    def colorCycle(self):
        pass
    
RGBstrip = LedStripControl(ledStrip)

while True:
    RGBstrip.setColor((255, 0, 0))
    sleep(1)
    RGBstrip.setColor((0, 255, 0))
    sleep(1)
    RGBstrip.setColor((0, 0, 255))
    sleep(1)
    RGBstrip.colorSnake((0, 255, 0), 5, 2000)
    RGBstrip.colorLineProgress((255, 255, 0), 2000)
    sleep(1)
    RGBstrip.clear()
    sleep(1)
    

