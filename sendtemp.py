import time
import ssd1306
import dht
import machine
from umqtt.robust import MQTTClient
from ubinascii import hexlify
import uasyncio
import util

thing = util.Thing()
messageCount = 0
sensor = dht.DHT11(machine.Pin(2))
i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5))
display = ssd1306.SSD1306_I2C(64, 64, i2c)
loop = uasyncio.get_event_loop()
pubclient = MQTTClient(thing.id, 'io.adafruit.com', 1883, 'ldaponte', '92cd28375c3aa9c92d0e7415b0af96740d38d586')
topic = 'ldaponte/feeds/iotclass.temperature'
interval = 5

'''
****************************** Support Functions ******************************
'''

def pushTemp():
    global messageCount
    
    sensor.measure()
    messageCount += 1

    message = str(messageCount)
    temp = str(sensor.temperature())
    humidity = str(sensor.humidity())

    displayTemp(message, temp, humidity)

    print('C: ' + message)
    print('T: ' + temp)
    print('H: ' + humidity)
    
    pubclient.publish(topic, str(sensor.temperature()), 0)
    loop.call_later(interval, pushTemp) # Schedule.

'''
****************************** Main functions ******************************
'''

# Display Temperature
def displayTemp(message, temp, humidity):
    display.fill(0)

    display.text('C: ' + message, 1, 20)
    display.text('T: ' + temp, 1, 35)
    display.text('H: ' + humidity, 1, 50)
 
    display.show()


pubclient.connect()
loop.call_soon(pushTemp) # Schedule after 2 seconds.
loop.run_forever()  