import time
import machine
import util
import neopixel
from umqtt.robust import MQTTClient
from ubinascii import hexlify

np = neopixel.NeoPixel(machine.Pin(4), 1)

def sub_callback(topic, msg):

    message = msg.decode('utf-8')
    print((topic, msg))

    np[0] = util.getRGBFromColor(message)

    np.write()

def run():
    thing = util.Thing()
 
    client = MQTTClient(thing.id, 'io.adafruit.com', 1883, 'ldaponte', '92cd28375c3aa9c92d0e7415b0af96740d38d586')
    topic = 'ldaponte/feeds/iotclass.setcolor'

    client.set_callback(sub_callback)
    client.connect()
    client.subscribe(topic, 0)

    button = machine.Pin(0)
    
    while True:
        if not button.value():  
            util.debounce(button)

            client.publish(topic, thing.color, 0)
            print('sent color', thing.color)

        time.sleep_ms(1)
        client.check_msg()
