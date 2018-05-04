import machine 
import neopixel
import util

np = neopixel.NeoPixel(machine.Pin(4), 1)

def set(red,green,blue):
    np[0] = util.getColor(red, green, blue)
        
    np.write()
