from evdev import InputDevice, categorize, ecodes, categorize, list_devices
from time import sleep
from utility import EcodeToCoordinate, CoordinateToNoteID

deviceList = [InputDevice(path) for path in list_devices()]
for device in deviceList:
    print(f"Path:{device.path}, Name:{device.name}, Phys:{device.phys}")

device = InputDevice("/dev/input/event0") # my keyboard
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        event = categorize(event)
        if event.keystate == 1:
            sleep(0.1)
            active_keys = device.active_keys()
            active_notes = [EcodeToCoordinate(key) for key in active_keys]
            active_note_id = [CoordinateToNoteID(coordinate) for coordinate in active_notes]
            print(f"Note pressed. Active Keys:{active_keys}. Active Notes:{active_notes}, ActiveNoteID:{active_note_id}")
        sleep(0.1)