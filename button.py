import time
import machine
from umqtt.robust import MQTTClient
from ubinascii import hexlify
import util

def run():
    thing = util.Thing()

    client = MQTTClient(thing.id, 'io.adafruit.com', 1883, 'ldaponte', '92cd28375c3aa9c92d0e7415b0af96740d38d586')
    client.connect()

    button = machine.Pin(0)

    while True:
        if not button.value():  
            util.debounce(button)

            client.publish('ldaponte/feeds/iotclass.lightswitch', 'toggle', 0)
            print('sent command to light')

        time.sleep_ms(1)
