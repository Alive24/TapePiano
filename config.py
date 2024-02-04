import copy
import json

defaultConfigDict = {
    "Debug": True,
    "keyboardControllerName": "Serial To HID",
    "prefixWait": 0.01,
    "suffixWait": 0.01,
    "actionTime": 2,
    "defaultRangeInSec": 30,
    "powerBarControlPinNum": 17
}


def loadConfig():
    try:
        configFile = open("/home/pi/Project/TapePiano/config.json",'r',encoding='utf-8')
        configDictToLoad = json.load(configFile)
        configDict = copy.deepcopy(defaultConfigDict)
        for key in list(configDictToLoad.keys()):
            configDict[key] = configDictToLoad[key]
        configFile.close()
    except Exception as e:
        print("loadConfig()错误")
        configDict = copy.deepcopy(defaultConfigDict)
        configFile = open("/home/pi/Project/TapePiano/config.json",'w',encoding='utf-8')
        json.dump(configDict,configFile)
        configFile.close()
    return configDict


def writeConfig(configDict):
    try:
        configFile = open("/home/pi/Project/TapePiano/config.json",'w',encoding='utf-8')
        json.dump(configDict,configFile)
        configFile.close()
    except Exception as e:
        print("writeConfig()错误")
        configFile = open("/home/pi/Project/TapePiano/config.json",'w',encoding='utf-8')
        json.dump(configDict,configFile)
        configFile.close()
    loadConfig()
    return