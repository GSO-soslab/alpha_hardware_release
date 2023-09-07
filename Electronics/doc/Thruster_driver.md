
## **Thruster driver board**
  ### Power input
  - The board can only be powered by 3.3v at `J8`
  
  ### Programming the MicroMod RP2040
  - Connect the two pins at `J11` to set the board to the boot mode before powering the system and connect the USB cable at `J10` 
  - Getting started document can be found [here](https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf)
  - RP2040 SDK is can be found in [pdf](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-c-sdk.pdf) or [web](https://raspberrypi.github.io/pico-sdk-doxygen/)
  - Pin map of the MicroMod RP2040  can be found [here](https://learn.sparkfun.com/tutorials/micromod-rp2040-processor-board-hookup-guide), and pin map of RP2040 is available [here](https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf)
  - The actual Pin number for the PWM ports and the Serial ports are listed in the following section.
  - `J12` is used for reset the board.

  ### Building pico code inside the build/xx folder
  ```
      mkdir build
      cd build
      cmake ..
      make hello_pio
   ```

  ### Function ports
  - RS232-1 (4pin JST): the uart0 (GP0-TX, GP1-RX on RP2040) is converted into a RS232 port at `J7`. 
    - Pin1 (white bar): GND
    - Pin2: 3.3V from the power
    - Pin3: TX
    - Pin4: RX

 - RS232-2 (4pin JST): the uart1 (GP8-Tx, GP9-Rx on RP2040) into RS232 at `J2`. 
    - Pin1 (white bar): GND
    - Pin2: 3.3V from the power
    - Pin3: TX
    - Pin4: RX

 
 - I2C (4pin JST): The board has one I2C communication port at `J5`. 
    - Pin1: GND
    - Pin2: 3.3V
    - Pin3: SDA (GP04 on RP2040)
    - Pin4: SCL (GP05 on RP2040)

- PWM channels (4pin JST): The board has 6 PWM channels at `J3`, `J4` and `J6` for controlling ESC and servo motors.
    - Pin1&2: GND
    - Pin3&4: PWM signal
    - J3: P3->GPIO24->4A, P4->GPIO13->6B
    - J4: P3->GPIO18->1A, P4->GPIO16->0A
    - J6: P3->GPIO22->3A, P4->GPIO20->2A
    - These pins could be configured as regular GPIO as well.

- Voltage sensing (VB at `J8`). User could sense the input voltage at VB pin through a voltage divider (100k omh and 10k omh in serial). The divided voltage is connected to GPIO26(ADC0) on the RP2040.
