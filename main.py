from pcf8575 import PCF8575
from utility import CountedNote, enableDriverPowerBar, getKeyboardPath, EcodeToCoordinate, CoordinateToNoteID, inspectionHelper, debugWithIndex, manualReversingWrapper
from time import sleep
from evdev import InputDevice, categorize, ecodes
from calibrateHelper import getCalibrateRatio
from itertools import groupby
import RPi.GPIO as GPIO
import asyncio

loop = asyncio.get_event_loop()

# Initialize I2C Ports
pcfList = []

# Initialize Objects
countedNoteList = []


# Initialize Manual Reversing
GPIO.add_event_detect(17, GPIO.BOTH, callback=lambda channel: manualReversingWrapper(channel, pcfList, loop, countedNoteList), bouncetime=300)


## Create PCF8575 objects in bulk
pcfBoardNum = 0
for port in range(0, 2):
    __pcfInPort = []
    for pcfAddress in range(0x20, 0x26):
        __targetPCFAddress = pcfAddress
        # if port == 1 and pcfAddress == 0x25:
        #     __targetPCFAddress = 0x27
        try:
            pcf = PCF8575(port, __targetPCFAddress)
            pcf.boardNum = pcfBoardNum
            pcf.port = [True] * 16
            pcf.port = [False] * 16
            __pcfInPort.append(pcf)
        except Exception as e:
            print(f"Failed to initialize pcf boards at port:{port}, targetPCFAddress:{__targetPCFAddress}", e)
        finally:
            pcfBoardNum += 1
    pcfList.append(__pcfInPort)




# Initialize Keyboard Controller
try:
    #device = InputDevice("/dev/input/event3")
    device = InputDevice(getKeyboardPath())
except Exception as e:
    print("Failed to get InputDevice:", e)



## Create CountedNote objects in bulk
for row in range(0, 11):
    __countedNoteRow = []
    for column in range(0, 8):
        try:
            noteID = row * 8 + column + 1
            __actionTimeMultiplier = 1
            # TODO: Calculate the correct __actionTimeMultiplier here            
            if noteID > 0:
                __actionTimeMultiplier = 1.85
            if noteID > 12:
                __actionTimeMultiplier = 1.3
            if noteID > 24:
                __actionTimeMultiplier = 0.9
            if noteID > 36:
                __actionTimeMultiplier = 0.5
            if noteID > 44:
                __actionTimeMultiplier = 1.85
            if noteID > 56:
                __actionTimeMultiplier = 1.3
            if noteID > 68:
                __actionTimeMultiplier = 0.9
            if noteID > 80:
                __actionTimeMultiplier = 0.5
            exec(f"note{noteID} = CountedNote(id={noteID}, coordinate=({row}, {column}), reverseActionTimeRatio=getCalibrateRatio({noteID}), actionTimeMultiplier={__actionTimeMultiplier})")
            __targetPort = 0
            __targetPCF = row
            if noteID > 44:
                __targetPort = 1
                __targetPCF = int((noteID - 45) / 8)
            exec(f"note{noteID}.bindPCFBoard(pcfList[{__targetPort}][{__targetPCF}])")
            exec(f"__countedNoteRow.append(note{noteID})")
        except Exception as e:
            print(f"Failed to create countedNoteList at row:{row}, column:{column}, noteId={row * 8 + column + 1}")
    countedNoteList.append(__countedNoteRow)



# Event Loop
async def main(device):
    try:
        enableDriverPowerBar(True)
        async for event in device.async_read_loop():
            taskList = []
            active_notes = []
            active_note_id = []
            if event.type == ecodes.EV_KEY:
                event = categorize(event)
                if event.keystate == 1:
                    try:
                        sleep(0.1)
                        active_keys = device.active_keys()
                        active_notes = [EcodeToCoordinate(key) for key in active_keys]
                        active_note_id = [CoordinateToNoteID(coordinate) for coordinate in active_notes]
                        print(f"Note pressed. Active Keys:{active_keys}. Active Notes:{active_notes}. Active Note in ID: {active_note_id}")
                    except Exception as e:
                        print(f"Failed to generate active notes to trigger, active_keys={active_keys}, active_notes={active_notes}, active_note_id={active_note_id}, Error: {e}")
                    triggerList = []
                    for note in active_notes:
                        triggerList.append(countedNoteList[note[0]][note[1]])
                    if triggerList:
                        triggerList.sort(key=lambda note: note.coordinate[0])
                    groupedTriggerList = []
                    for pcfBoardNum, notesToTrigger in groupby(triggerList, key=lambda note: note.PCFBoard.boardNum):
                        noteInGroup = [note for note in notesToTrigger]
                        print(f"Debugging groupedTriggerList: {pcfBoardNum}, {noteInGroup} ")
                        groupedTriggerList.append(noteInGroup)
                    while groupedTriggerList:
                        groupedTriggerList = [group for group in groupedTriggerList if group]
                        __CurrentNotesToTriggerList = []
                        for group in groupedTriggerList:
                            print(f"Debugging, Split __CurrentNotesToTriggerList = {__CurrentNotesToTriggerList}")
                            __CurrentNotesToTriggerList.append(group.pop())                           
                        __CurrentTaskList = [asyncio.create_task(note.trigger()) for note in __CurrentNotesToTriggerList]
                        if __CurrentTaskList:
                            try:
                                await asyncio.gather(*__CurrentTaskList)
                            except Exception as e:
                                print(f"Failed to gather trigger tasks. taskList={taskList}, __CurrentNotesToTriggerList = {__CurrentNotesToTriggerList}, groupedTriggerList:{groupedTriggerList}, Error={e},")
                            finally:
                                print(f'Debugging, clearing groupedTriggerList')       
                sleep(0.1)
    except Exception as e:
        print(f"Main Function failed. Error:{e}")
    finally:
        GPIO.cleanup()
        enableDriverPowerBar(False)

# Program Entry
loop.run_until_complete(main(device))
