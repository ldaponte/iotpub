
import ssd1306
import ntptimes
import utime
import time
import machine

def run():
    screenW = 64
    screenH = 48

    i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5))
    display = ssd1306.SSD1306_I2C(screenW, screenH, i2c)

    lastSecond = 0
    hour = 3600
    column = 1
    row = 20

    ntptimes.settime('ch.pool.ntp.org')

    while True:
        display.fill(0) # Clear display
        toffset = utime.time() + (hour * 2)  # UTC + 2
        (year, month, day, hour, minute, second, weekday, yearday) = utime.localtime(toffset)
        if second != lastSecond:
            display.text('{}/{}/{}'.format(day, month, year), column , row)
            display.text('{:02d}:{:02d}:{:02d}'.format(hour, minute, second), column, row + 20)
            display.show()
            lastSecond = second

        time.sleep_ms(100)
