from pcf8575 import PCF8575
from config import loadConfig
import asyncio
from copy import deepcopy
import evdev
from time import sleep
import RPi.GPIO as GPIO
from itertools import groupby


# Initialize GPIO for driver power control. Initially Low.
try:
    GPIO.cleanup()
except Exception as e:
    print(f"No need to cleanup GPIO: {e}")
finally:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

## Status Store for Manual Reversing
manualReversingStore = 0




config = loadConfig()

class CountedNote:
    def __init__(self, id:int, coordinate:tuple, count:int=0, reverseActionTimeRatio:float=1, actionTimeMultiplier:float=1):
        self.id = id
        self.count = 0
        self.coordinate = coordinate
        self.PCFBoard = None
        self.reverseActionTimeRatio = reverseActionTimeRatio  # Calibrate for the same distance for opposite direction
        self.actionTimeMultiplier = actionTimeMultiplier
        self.rangeInPulse = int(config['defaultRangeInSec'] / config['actionTime'])
    def resetCount(self):
        self.count = 0
    def getDirection(self):
        __remainder = self.count % (self.rangeInPulse * 2)
        direction = -1
        if __remainder <= self.rangeInPulse:
            direction = 1
        if __remainder == 0:
            direction = -1
        return direction
    def bindPCFBoard(self, PCFBoard:PCF8575):
        self.PCFBoard = PCFBoard
    async def executeMovement(self, direction):
        outputIndex = self.coordinate[1]
        __noteID = CoordinateToNoteID(self.coordinate)
        if __noteID > 44:
            outputIndex = (__noteID + 3) % 8
        pin1Index = 15 - 2 * outputIndex
        pin2Index = pin1Index - 1
        if not self.PCFBoard:
            print("PCFBoard not bound yet.")
        __targetPort = [False] * 16
        __targetActionTimeRatio = self.reverseActionTimeRatio
        if direction == 1:
            __targetPort[pin1Index] = True
            __targetPort[pin2Index] = False
            # if __noteID == 42 :
            #     __targetPort[pin1Index] = False
            #     __targetPort[pin2Index] = True
            __targetActionTimeRatio = 1
        if direction == -1:
            __targetPort[pin1Index] = False
            __targetPort[pin2Index] = True
        self.PCFBoard.port = __targetPort
        __targetActionTime = config["actionTime"] * __targetActionTimeRatio * self.actionTimeMultiplier 
        if config['Debug']:
            print(f"Executing Movement by countedNote#{self.id}. PCFBoard = {self.PCFBoard}, Pin 1 = {pin1Index}, Pin 2 = {pin2Index}, currentCount = {self.count}, direction = {direction}, targetActionTime={__targetActionTime}")
        await asyncio.sleep(__targetActionTime)
        self.PCFBoard.port = [False] * 16
        return
    async def trigger(self):
        print(f"Triggering {self.id}")
        self.count += 1
        __direction = self.getDirection()
        await self.executeMovement(__direction)

def EcodeToCoordinate(ecode:int) -> tuple:
    ecodeToCoordinateList:dict = [
        [30, 48, 46, 32, 18, 33, 34, 35],
        [23, 36, 37, 38, 50, 49, 24, 25],
        [16, 19, 31, 20, 21, 47, 17, 45],
        [21, 44, 2, 3, 4, 5, 6, 7],
        [8, 9, 10, 11, 28, 1, 14, 15],
        [57, 12, 13, 26, 27, 43, 39, 40],
        [41, 51, 52, 53, 58, 59, 60, 61],
        [62, 63, 64, 65, 66, 67, 68, 87],
        [88, 99, 70, 119, 110, 102, 104, 111],
        [107, 109, 106, 105, 108, 103, 69, 98],
        [55, 74, 78, 96, 79, 80, 81, 75],
        [76, 77, 71, 72, 73, 82, 83]
    ]
    # Make modification here.
    ecodeToCoordinateList[2][4] = 76
    for column in range(0, 12):
        for row in range(0, 8):
            try:
                if ecode == ecodeToCoordinateList[column][row]:
                    return (column, row)
            except Exception as e:
                print(f"Failed to return coordinate. Ecode={ecode}, row={row}, column={column}")
    print(f"Failed to find key for ecode:{ecode}")
    return (None, None)

def CoordinateToNoteID(coordinate:tuple):
    id = 0
    id = coordinate[0]*8 + coordinate[1] + 1
    return id

def getKeyboardPath() -> str:
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if config["keyboardControllerName"] in device.name:
            return device.path
    print("Can't Find Keyboard!")
    return None

def inspectionHelper(pcfList):
    while True:
        try:
            for board in pcfList:
                for pcf in board:
                    pcf.port = [False, True] * 8
            sleep(5)
            for board in pcfList:
                for pcf in board:
                    pcf.port = [True, False] * 8
            sleep(4)
            for board in pcfList:
                for pcf in board:
                    pcf.port = [False, False] * 8
            sleep(0.5)
        except Exception as e:
            print(f"Inspection Failed. Error Code:{e} board:{board}, pcf:{pcf}")

def enableDriverPowerBar(value=True):
    if value:
        GPIO.output(18, GPIO.HIGH)
    else:
        GPIO.output(18, GPIO.LOW)

def debugWithIndex(pcfList, port, pcfAddress, index):
    pin1Index = 15 - 2 * index
    pin2Index = pin1Index - 1
    __targetPortValue = [False] * 16
    __targetPortValue[pin1Index] = True
    __targetPortValue[pin2Index] = False
    pcfList[port][pcfAddress].port = __targetPortValue
    __targetPortValue = [False] * 16
    sleep(1)
    __targetPortValue[pin1Index] = False
    __targetPortValue[pin2Index] = True
    pcfList[port][pcfAddress].port = __targetPortValue
    __targetPortValue = [False] * 16
    sleep(1)
    __targetPortValue[pin1Index] = False
    __targetPortValue[pin2Index] = False
    pcfList[port][pcfAddress].port = __targetPortValue
    __targetPortValue = [False] * 16
    
async def triggerFromActiveNotes(pcfList:list=[], countedNoteList:list=[], active_notes:list=[]):
    active_notes.sort(key=lambda note: note[0])
    for row, notesToTrigger in groupby(active_notes, key=lambda note: note[0]):
        print(row, [note for note in notesToTrigger])
        __noteID = CoordinateToNoteID(note)
        __port = 0 if row < 6 else 1
        __pcfIndex = row if row < 6 else (row - 6)
        __outputIndexList = [note[1] for note in notesToTrigger]
        __targetPortValue = [False] * 16
        for outputIndex in __outputIndexList:
            pin1Index = 15 - 2 * outputIndex
            pin2Index = pin1Index - 1
            if countedNoteList[__port][outputIndex].get_direction() == 1:
                __targetPortValue[pin1Index] = True
                __targetPortValue[pin2Index] = False
            else:
                __targetPortValue[pin1Index] = False
                __targetPortValue[pin2Index] = True
        pcfList[__port][__pcfIndex].port = __targetPortValue
        # await asyncio.sleep(config["actionTime"] * self.actionTimeRatio)
        await asyncio.sleep(config["actionTime"])
        pcfList[__port][__pcfIndex].port = [False * 16]
    pass

def manualReversingWrapper(channel, pcfList, loop, countedNoteList):
    global manualReversingStore
    sleep(0.3)
    manualReversingTarget = GPIO.input(17)
    # if config["Debug"]:
    #     print(f"Debugging Manual Reversing. Target:{manualReversingTarget}, Store:{manualReversingStore}, channel:{channel}")
    if manualReversingTarget != manualReversingStore:
        print(f"Setting Manual Reversing to {manualReversingTarget}.")
        loop.call_soon_threadsafe(lambda: manualReversing(pcfList, bool(manualReversingTarget)))
        manualReversingStore = manualReversingTarget
    for row in countedNoteList:
        for note in row:
            note.count = 0

def manualReversing(pcfList, active=False):
    if config['Debug']:
            print(f"Executing Manual Reversing Control, targetState={active}")
    if active:
        for port in pcfList:
            for pcfBoard in port:
                pcfBoard.port = [True, False] * 8
#                if pcfBoard.boardNum == 5:
#                    pcfBoard.port = [True, False, True, False, True, False, True, False, True, False, True, False, False, True, True, False]
                sleep(5)
                pcfBoard.port = [False] * 16
                sleep(0.1)
    else:
        for port in pcfList:
            for pcfBoard in port:
                pcfBoard.port = [False, False] * 8

