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

![2e7a021c3c729ed21e8aebc752ce00b](https://github.com/Alive24/TapePiano/assets/20827211/4569de94-c147-427e-9755-57bb95427d8b)
![91758de8f6b7c3c00a45a66d360fdd0](https://github.com/Alive24/TapePiano/assets/20827211/5e2b27bc-4c85-44ee-90de-e1b9cf2fe465)
![7c96d30a25132c5dd5f5c37ae3b0a68](https://github.com/Alive24/TapePiano/assets/20827211/4af85cc3-408b-4ff6-8e19-e9acf6d72cf9)
![367f51ef411df973dab55cdfa26f954](https://github.com/Alive24/TapePiano/assets/20827211/1164de34-0869-495e-bd05-0ea140325da7)
![aee9f7d52f968d2f6bc9fcc282924cd](https://github.com/Alive24/TapePiano/assets/20827211/b8939691-bd44-4341-ba59-9ca951f2f4d1)
![82b0669ecaf5aa51a42f52967bddb33](https://github.com/Alive24/TapePiano/assets/20827211/8a091e95-918c-4c3f-8f00-d3ff21fb7919)
![aa076145261cb3d9b47bd14301fcfbd](https://github.com/Alive24/TapePiano/assets/20827211/ad5f6300-27da-4bc6-baa9-be9784503b9e)
![ba06f5a409e59d0935ea4b96bf68079](https://github.com/Alive24/TapePiano/assets/20827211/dbc5372d-7af8-40be-b408-ebc74339dc8f)
![22b01775bf4923f0c8a1210e68570a0](https://github.com/Alive24/TapePiano/assets/20827211/4c76c7b9-71f5-4565-80ce-679257efd6b3)
![d878ac95f2a96f7d4757b9667f55597](https://github.com/Alive24/TapePiano/assets/20827211/87383c5c-a9ec-4374-9979-9ff925c88f0f)
![9d0d21386082fd3b39db6809b36c14b](https://github.com/Alive24/TapePiano/assets/20827211/d553f5f0-2645-458f-8b4b-6c653ef925d9)
![cde9a91e501178a50abf16ebfb3333f](https://github.com/Alive24/TapePiano/assets/20827211/7ca4973b-ccc1-4cac-a2b8-e3695dcc097f)
![23c8d8c4b505ef8f0fe853189c9cd52](https://github.com/Alive24/TapePiano/assets/20827211/84642647-e2c5-483e-9745-823b7292de87)


## Videos
https://youtu.be/Js4PpYcqvtc
https://youtu.be/KsCReLSWoyQ
