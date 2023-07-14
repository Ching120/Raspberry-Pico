import machine
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import utime


led = Pin(25, Pin.OUT)
to_volts = 3.3 / 65535
temper_sensor = machine.ADC(4)

first_proofing_temp = 24  # 第一次發酵溫度（攝氏度）
first_proofing_temp_tolerance = 0.5  # 溫度容許範圍（攝氏度）
first_proofing_time = 20  # 第一次發酵時間（分鐘）
intermediate_proofing_temp = 24.5  # 中間發酵溫度（攝氏度）
intermediate_proofing_temp_tolerance = 0.5  # 溫度容許範圍（攝氏度）
intermediate_proofing_time = 10  # 中間發酵時間（分鐘）
second_proofing_temp = 25  # 第二次發酵溫度（攝氏度）
second_proofing_temp_tolerance = 0.5  # 溫度容許範圍（攝氏度）
second_proofing_time = 30  # 第二次發酵時間（分鐘）

i2c = I2C(0, sda=Pin(0), scl=Pin(1))
lcd = I2cLcd(i2c, 0x3F, 2, 16)

def display_message(message):
    lcd.clear()
    lcd.putstr(message)

def start_timer(duration):
    remaining_time = duration
    while remaining_time > 0:
        lcd.move_to(0, 1)
        lcd.putstr("Time: {} sec".format(remaining_time))
        utime.sleep(1)  # 等待1秒
        remaining_time -= 1
    lcd.move_to(0, 1)
    lcd.putstr("Well done!")

completed_proofings = 0
is_first_displayed = False


while True:
    temper_volts = temper_sensor.read_u16() * to_volts
    celsius_degrees = 27 - (temper_volts - 0.706) / 0.001721

    if not is_first_displayed:
        lcd.clear()
        lcd.putstr("HELLO CHEF!")
        lcd.move_to(0, 1)
        lcd.putstr('Temp: {}oC'.format(round(celsius_degrees, 1)))
        utime.sleep(5)
        is_first_displayed = True
    else:
        lcd.move_to(0, 1)
        lcd.putstr('Temp: {}oC'.format(round(celsius_degrees, 1)))

    if completed_proofings == 0:
        if celsius_degrees < first_proofing_temp - first_proofing_temp_tolerance:
            lcd.clear()
            lcd.putstr('1.Temp: {}oC'.format(round(celsius_degrees, 1)))
            lcd.move_to(0, 1)
            lcd.putstr("Low, heat up")
            led.on()
        elif celsius_degrees > first_proofing_temp + first_proofing_temp_tolerance:
            lcd.clear()
            lcd.putstr('1.Temp: {}oC'.format(round(celsius_degrees, 1)))
            lcd.move_to(0, 1)
            lcd.putstr("HOT, cool down")
            led.on()
        else:
            led.off()
            display_message("1 proofing")
            start_timer(first_proofing_time)
            lcd.clear()
            display_message("Well done!")
            completed_proofings += 1
    elif completed_proofings == 1:
        if celsius_degrees < intermediate_proofing_temp - intermediate_proofing_temp_tolerance:
            lcd.clear()
            lcd.putstr('1/2.Temp: {}oC'.format(round(celsius_degrees, 1)))
            lcd.move_to(0, 1)
            lcd.putstr("Low, heat up")
            led.on()
        elif celsius_degrees > intermediate_proofing_temp + intermediate_proofing_temp_tolerance:
            lcd.clear()
            lcd.putstr('1/2.Temp: {}oC'.format(round(celsius_degrees, 1)))
            lcd.move_to(0, 1)
            lcd.putstr("HOT, cool down")
            led.on()
        else:
            led.off()
            display_message("1/2 proofing")
            start_timer(intermediate_proofing_time)
            lcd.clear()
            display_message("Well done!")
            completed_proofings += 1
    elif completed_proofings == 2:
        if celsius_degrees < second_proofing_temp - second_proofing_temp_tolerance:
            lcd.clear()
            lcd.putstr('2.Temp: {}oC'.format(round(celsius_degrees, 1)))
            lcd.move_to(0, 1)
            lcd.putstr("Low, heat up")
            led.on()
        elif celsius_degrees > second_proofing_temp + second_proofing_temp_tolerance:
            lcd.clear()
            lcd.putstr('2.Temp: {}oC'.format(round(celsius_degrees, 1)))
            lcd.move_to(0, 1)
            lcd.putstr("HOT, cool down")
            led.on()
        else:
            led.off()
            display_message("2 proofing")
            start_timer(second_proofing_time)
            lcd.clear()
            display_message("Well done!")
            completed_proofings += 1

    if completed_proofings >= 3:
        display_message("YOUR BREAD IS")
        lcd.move_to(0, 1)
        lcd.putstr("PERFECT!!")
        utime.sleep(10)
        completed_proofings = 0  # 重置發酵階段計數器
        is_first_displayed = False  # 重置首次顯示旗標

    utime.sleep(20)  # 等待20秒


