
## **SBC HAT RISE no USB**
  This is the same as the SBC HAT RISE. However we removed the USB hub and add 4 more UART/RS232 ports.

  To enable all 4 I2C to UART chips, you need to edit `config.txt` file by adding the following lines.

  ```
#RS232 1&2 
dtoverlay=sc16is752-i2c,int_pin=23,addr=0x48
#RS232 3&4
dtoverlay=sc16is752-i2c,int_pin=24,addr=0x4C
#RS232 5&6 
dtoverlay=sc16is752-i2c,int_pin=25,addr=0x49
#RS232 7&8
dtoverlay=sc16is752-i2c,int_pin=22,addr=0x4D
  ```
  The port and connector index is listed below

  J14 = ttySC6

  J15 = ttySC7
  
  J9 = ttySC4
  
  J10 = ttySC5
  
  J4 = ttySC2
  
  J5 = ttySC3
  
  J8 = ttySC1
  
  J7 = ttySC0
  
  More information about how to iinstall the kernel drivers and test the serial ports can be found in the [SBC_HAT_RISE documentation](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/SBC_HAT_RISE.md)