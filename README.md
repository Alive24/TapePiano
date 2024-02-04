# TapePiano

This the archived source code of the controlling software for the the art project *Distance of Sound* by [Shen Shaomin](https://en.wikipedia.org/wiki/Shen_Shaomin).

It has been publicly exhibited and scheduled for more exhibitions in the future, including Art Shenzhen 2023 at Hall 6, Shenzhen Convention & Exhibition Center in September 2023. It has been publicly covered in multiple media, including [Art Shenzhen](https://mp.weixin.qq.com/s/xibU71yUhfo1dbHxoiUPHg) as one of the public art projects and [SZTV News](https://mp.weixin.qq.com/s/USHdcssANFCf1vWlJYQphQ)

## Architecture

The art project is a modern re-creation of a deprecated piano for which we attached a brand new mechanic box that contains 88 motor-driven measuring tapes and a complete array of controlling units including a Raspberry Pi, custom-made PCBs for I/O mapping, magnetic sensors on the key notes, motor driving units, power supplies, etc.

With the code archived in this repo, it would be able to detect and register all key strikes, and properly map strikes to the corresponding motor-driven tapes, and drive the tapes to the correct positions. It also supports individual calibrating for each tape to offset the variations in the sensitivity of each magnetic sensor, motor driving unit, and the motor itself.

## Key Components Used

- Raspberry Pi
- L290N
- Reed Switches

## Pictures 