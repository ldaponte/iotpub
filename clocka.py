
import ssd1306
import ntptimes
import utime
import time
import machine
import util

def run():
    screenW = 64
    screenH = 48

    i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5))
    display = ssd1306.SSD1306_I2C(screenW, screenH, i2c)

    lastSecond = 0
    hour = 3600

    ntptimes.settime('ch.pool.ntp.org')

    while True:
        toffset = utime.time() + (hour * 2)  #UTC + 2
        (year, month, day, hour, minute, second, weekday, yearday) = utime.localtime(toffset)

        if second != lastSecond:
            util.drawFace(display, screenW, screenH)
            util.drawArms(display, screenW, screenH, hour, minute, second)
            display.show()
            lastSecond = second

        time.sleep_ms(100)
