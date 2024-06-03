### First-time boot-up setup (HDMI and keyboard needed)

- username: `mvp_admin`, password: `temppwd`

- `hostname -I` or `ip -a address` to check current IP
- Edit the netplan `sudo nano /etc/netplan/50-cloud-init.yaml`
- add `addresses: [192.168.1.124/24]`
- `ping google.com`
- Disable auto update `sudo dpkg-reconfigure -plow unattended-upgrades`

### Open I2C port

- `sudo apt update`
- `sudo apt install raspi-config`
- `sudo raspi-config`
- Go to `Interface Options` > `I2c` enable it
- Go to `Interface Opetions` > `SPI` disable it



### Setup I2C UART Chip (sc16is752-i2c)

- Install libraries

  ```
  sudo apt-get install -y make
  sudo apt-get install build-essential
  ```

  ```
  wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz
  tar zxvf bcm2835-1.71.tar.gz 
  cd bcm2835-1.71/
  sudo ./configure
  sudo make
  sudo make check
  sudo make install
  #For more details, please refer to http://www.airspayce.com/mikem/bcm2835/
  ```

  ```
  sudo apt-get install python3-dev
  sudo apt-get install python3-rpi.gpio
  sudo apt-get install python3-smbus
  ```

- Add device using `dtoverlay`

  - `sudo nano /boot/firmware/config.txt`

  - add the following lines at the end

    ```
    #RS232 1&2 SC6, SC7
    dtoverlay=sc16is752-i2c,int_pin=23,addr=0x48
    #RS232 3&4 SC4, SC5
    dtoverlay=sc16is752-i2c,int_pin=24,addr=0x4C
    ##the last two is for the 8 RS232 version
    #RS232 5&6 SC2 SC3
    dtoverlay=sc16is752-i2c,int_pin=25,addr=0x49
    #RS232 7&8 SC0 SC1
    dtoverlay=sc16is752-i2c,int_pin=22,addr=0x4D
    ```

  - `sudo reboot`

- Check new serial ports

  - `ls /dev/ttySC*`

  - If you see SC0, SC1 ..... and so on, then you are good.

    | Connector | Dev    |
    | --------- | ------ |
    | J8        | ttySC0 |
    | J7        | ttySC1 |
    | J4        | ttySC2 |
    | J5        | ttySC3 |
    | J9        | ttySC4 |
    | J10       | ttySC5 |
    | J14       | ttySC6 |
    | J15       | ttySC7 |

  - Test with `minicom`

  - `sudo minicom -s`
    - `ctrl+A` then `o`: configure the port
    - `ctrl+A` then `x` : exit the program.

### GPIO conifguration 

On the hat we have 5 GPIOs (7,8, 9, 12, 13). We use the GPIO as output pins to control MOSFET and power supplies to control sensor payloads. GPIO9, 12, 13 can be configured as normal GPIO.

- First, you need to export the GPIO

```
echo 9 > /sys/class/gpio/export
```

- Second, you can set the direction of the GPIO

```
echo out > /sys/class/gpio/direction
```

- Finally, you can set the GPIO to High[1] or Low [0]

```
echo 1 > /sys/class/gpio/direction
```

***Note***: For GPIO7  and GPIO8, they are originally used as chip select pin for SPI in the PI system. To free them to become a regular GPIO, you need to add the  following line in `/boot/config.txt` and `/boot/firmware/config.txt` file after the line `dtparam=spi=off`. The added line will remapp the chip select pin to other GPIOs, i.e., 20 and 21 here. Then, you can reboot the PI, and `GPIO7` and `GPIO8` can be used as normal GPIOs.

```
dtoverlay=spi0-cs,cs0_pin=20,cs1_pin=21
```

### Install ROS Humble

[Reference](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)

- add source bash into your ~/.bashrc 

- only install the base `sudo apt install ros-humble-ros-base`

- install the demo_node packages to test ros 

  ```
  sudo apt install ros-humble-demo-nodes-cpp
  sudo apt install ros-humble-demo-nodes-py
  ```

### Test ADC chip (MCP3422)

### Test Bar30 pressure sensor

### Test XSense MTI 



## PWM Driver add-on Board

### Configure Real-time clock (DS3231)

- Install `i2c-tools`
- `i2cdetect -y 1` to scan the device on the i2c bus and get their address
- scan the port make sure the devices are there.
- The I2C address of the clock should be `0x68`

[Reference](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-up-and-test-i2c)

### Configure the PWM chip (PCA9685)

- The I2C address should be `0x40` and `0x70`, the later one is the default all channel address.



## Install MVP Framework

### MVP messages

### MVP Control

### MVP Mission

### MVP Core (ALPHA_core for ROS Noetic)









