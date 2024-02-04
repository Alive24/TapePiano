from machine import Pin
from time import sleep

pin1 = Pin(21, Pin.OUT, Pin.PULL_DOWN)
pin2 = Pin(19, Pin.OUT, Pin.PULL_DOWN)
pin1.value(0)
pin2.value(0)
HallPin = Pin(17, Pin.IN, Pin.PULL_UP)
actionTimeRatio = 1.5
testingTimeRange = 15
print("Starting testing in 5 sec")
sleep(5)

print("Starting!")


def trigger(direction, HallPin):
    if direction == 1:
        pin1.value(0)
        pin2.value(1)
    if direction == -1:
        pin1.value(1)
        pin2.value(0)
    while True:
        sleep(0.1)
        __HallPinValue = HallPin.value()
        if not __HallPinValue:
            sleep(0.1)
            pin1.value(0)
            pin2.value(0)
            break
        
while True:
    trigger(1, HallPin)
    sleep(2)
    trigger(1, HallPin)
    sleep(2)
    trigger(1, HallPin)
    sleep(2)
    trigger(1, HallPin)
    sleep(2)
    trigger(1, HallPin)
    sleep(2)
    trigger(-1, HallPin)
    sleep(2)
    trigger(-1, HallPin)
    sleep(2)
    trigger(-1, HallPin)
    sleep(2)
    trigger(-1, HallPin)
    sleep(2)
    trigger(-1, HallPin)
    sleep(2)
