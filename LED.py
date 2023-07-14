
from machine import Pin, Timer #在machine模組下,import Timer 類別
led = Pin(25, Pin.OUT) #建立Pin物件，名稱叫led
timer = Timer() #建立Timer(定時器)的物件

def blink(timer): #計時器
    led.toggle()

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink) #初始化 timer

#freq頻率：觸發頻率2.5赫茲 EX:頻率為3Hz,則表示波形在 1 秒內重複3次。
#mode模式：可以選擇一次觸發Timer.ONE_SHOT或是週期性觸發Timer.PERIODIC
#callback：當 Timer 觸發時,要呼叫的函數,沒有的話,填入None。
