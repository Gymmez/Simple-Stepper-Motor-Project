from machine import Pin
from time import sleep
import time

Step = Pin(19, Pin.OUT)
Dir = Pin(18, Pin.OUT)
Ms1 = Pin(23, Pin.OUT)
Ms2 = Pin(22, Pin.OUT)
Ms3 = Pin(21, Pin.OUT)
Trig = Pin(15, Pin.OUT)
Echo = Pin(4, Pin.IN)
Led = Pin(2, Pin.OUT)

Dir.value(0)

#Control the microstepping mode
Ms1.value(0)
Ms2.value(1)
Ms3.value(0)

def get_distance():
    Trig.value(0)
    time.sleep_us(2)
    Trig.value(1)
    time.sleep_us(10)
    Trig.value(0)

    start_wait = time.ticks_us()
    while Echo.value() == 0:
        if time.ticks_diff(time.ticks_us(), start_wait) > 30000:
            return 999 
    start = time.ticks_us()

    while Echo.value() == 1:
        if time.ticks_diff(time.ticks_us(), start) > 30000:
            return 999
    end = time.ticks_us()

    duration = time.ticks_diff(end, start)
    return (duration * 0.0343) / 2

def led_flashing():
    for _ in range(3):
        Led.value(1)
        sleep(0.05)
        Led.value(0)
        sleep(0.05)

while True:
    Dir.value(1 - Dir.value())

    for _ in range(400):
        Step.value(1)
        sleep(0.02)
        Step.value(0)

        d = get_distance()
        if d < 20:
            led_flashing()

        sleep(0.02)

