# PI setup guide for the ALPHA RISE SBC HAT
## Create Ubuntu 20.04 image.
- Open **Raspberry Pi Imager** 
- Choose **Other general-purpose OS** 
- Select **Ubuntu**
- Scroll down **Ubuntu Server 20.04.5 LTS(64-bit)** option
- Click the Advanced options icon at the right-bottom corner
    - Check **Set hostname**
    - Check **Enable SSH**, select **Use password authentication**
    - Check **Set username and password**, type in the username and password you want for ssh login later on. For example, username: `alpha`, password: `temppwd`.
    - Check **Configure wireless LAN**, type in the network name and password in **SSID** and **Password**, Select the corresponding **Wireless LAN country**
    - **Save** once finished.
- Select the SDCard, then **write** the image.

## First time booting up
- Get a micro-HDMI cable to connect the PI to a monitor
- Get a usb keyboard to connect to the PI's usb.
- Plug in the power
- Login using the username and password you set.
- Network setup:
    - Setup a static IP for wifi:
        - `sudo nano /etc/netplan/50-cloud-init.yaml`
        - add changes: wifi replace encrypt-password
        ```yaml
        network: 
            version: 2
            wifis:
                renderer: networkd
                wlan0:
                    access-points:
                        soslab:
                            password: encrypt-password 
                    dhcp4: no 
                    addresses: [192.168.1.111/24]
                    nameservers:
                        addresses: [192.168.1.1, 8.8.8.8]
                    gateway4: 192.168.1.1
        ```
        - apply the changes:
        ```shell
        sudo netplan generate
        sudo netplan apply
        sudo reboot
        ```
    - Enable netowrk for Fin(USB wifi) and Ethernet:
        - `sudo nano /etc/netplan/50-cloud-init.yaml`
        - add changes: comment out `wlan0` for the original PI wifi
        ```yaml
        network:
        version: 2
        wifis:
            renderer: networkd
            #wlan0:
            #    access-points:
            #        soslab:
            #            password: encrypt-password 
            #    dhcp4: no 
            #    addresses: [192.168.1.111/24]
            #    nameservers:
            #        addresses: [192.168.1.1, 8.8.8.8]
            #    gateway4: 192.168.1.1
            wlan1:
                access-points:
                    soslab:
                        password: encrypt-password 
                dhcp4: no 
                addresses: [192.168.1.121/24]
                nameservers:
                    addresses: [192.168.1.1, 8.8.8.8]
                gateway4: 192.168.1.1
        ethernets:
            eth0:
                dhcp4: no 
                addresses: [192.168.2.121/24]
        ```
        - apply same changes
        ```sh
        sudo netplan generate
        sudo netplan apply
        sudo reboot
        ```
    - type `hostname -I` or `ip -a address`, you should see the new IP of your PI now.

    - Note: if you want to use ethernet port on the PI to access internet, you need to comment out `nameservers` and `gateway4` line under `wlan1` and add proper address under `eth0` 

- You can disable the auto update:
    ```
    sudo dpkg-reconfigure -plow unattended-upgrades
    ```
## Test the USB Hub
- You can solder the jumper JP1 to power the USB Hub chip. The middle pad is connected to the USB Hub Vcc, the one with an arrow is the pad connected to 5V PI input, and the other one is connected to the USB upstream 5v. For teting your can solder the USB Hub Vcc to the upstream power.
- Use a micro usb cable to plug into the upstream usb port. 
- Plug in any USB device to other ports. You should be able to see the device if the board is working. Meanwhile, you should see LEDs are on to indicate a device is detected on a port.

## USB device udev rules
- For GPS:
    - find usb port: 
    ```sh
    dmesg | greb cp210
    ```
    - find device information: 
    ```sh
    # replace the # with your usb device number
    sudo udevadm test $(udevadm info -q path -n /dev/ttyUSB#) 
    ```
    - generate udev rules: may has conflict with gpio, check [reference](https://github.com/raspberrypi/linux/issues/3989)
    ```sh
    # replace idVendor and idProduct from last step
    sudo bash -c 'echo "SUBSYSTEM==\"tty\", ACTION==\"add\", ATTRS{idVendor}==\"10c4\", ATTRS{idProduct}==\"ea60\", SYMLINK+=\"alpha_gps\"" > /etc/udev/rules.d/99-usb-gps.rules'
    ```
    - reboot to enable rules
    - check SYMLINK: `ls -l /dev/alpha_gps`
- For RF:
    - find us port:
    ```sh
    dmesg | greb ch341
    ```
    - find device information: 
    ```sh
    # replace the # with your usb device number
    sudo udevadm test $(udevadm info -q path -n /dev/ttyUSB#) 
    ```
    - generate udev rules:
    ```sh
    # replace idVendor and idProduct from last step
    sudo bash -c 'echo "SUBSYSTEMS==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\"1a86\", ATTRS{idProduct}==\"7523\", SYMLINK+=\"alpha_rf\"" > /etc/udev/rules.d/99-usb-rf.rules'
    ```
    -  reboot to enable rules
    -  check SYMLINK: `ls -l /dev/alpha_rf`
  
## Raspi-config ##
If you are using Ubuntu you may not have raspi-config for enabling ports for the PI.
You can simply type `sudo raspi-config` in the terminal to see if you have it or not.

If you don't have it, you can following the instruction here to install it.
```
wget https://archive.raspberrypi.org/debian/pool/main/r/raspi-config/raspi-config_20200601_all.deb -P /tmp
sudo apt-get install libnewt0.52 whiptail parted triggerhappy lua5.1 alsa-utils -y
# Auto install dependancies on eg. ubuntu server on RPI
sudo apt-get install -fy
sudo dpkg -i /tmp/raspi-config_20200601_all.deb
```

## Enable and test I2C ports
- Open a terminal and type in 
```sudo raspi-config ```
- In the window, choose Interfacing Options -> I2C ->yes 
- Reboot the PI, ```sudo reboot```
- You can plug-in a I2C device, e.g., the [pressure sensor](https://bluerobotics.com/store/sensors-sonars-cameras/sensors/bar30-sensor-r1/) from Blue Robotics. And use the [python script](https://github.com/bluerobotics/ms5837-python) to validate if your PI can talk to the sensor.

## Enable the I2C to dual UART ICs and test RS232 ports
The original instruction is available here from [waveshare](https://www.waveshare.com/wiki/Serial_Expansion_HAT). The major change is the use of `python3` prefix and the way we edit the `config.txt` for Ubuntu image.
Our RS232 Ports are created from the I2C bus. If you have enabled I2C in the above step, you don't have to enable it again.
- Install make and build
```
    sudo apt-get install -y make
    sudo apt-get install build-essential
```
- Install libraries
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
- Install WiringPi libraries
```
sudo apt-get install wiringpi

#For Pi 4 with Pi OS image, you need to update it：
cd /tmp
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
gpio -v
#You will get 2.52 information if you install it correctly
```
- **IMPORTANT: Ubuntu user**
    - Download the release from `https://github.com/WiringPi/WiringPi/releases`. Make sure you used the `-arm64.deb` version
    - copy from your local computer to the Pi use `scp`, then install it.
        ```
        scp wiringpi-2.61-g.deb alpha@192.168.1.110:
        sudo dpkg -i wiringpi-latest.deb`
        gpio -v
        ```

- Install python packages (you need to use `python3` prefix if you are using python3)
```
sudo apt-get install python3-dev
sudo apt-get install python3-rpi.gpio
sudo apt-get install python3-smbus
```

- Configure the I2C to UART IC
    - Edit the boot/config.txt (**for Ubuntu, you can directly edit the config.txt in the SD Card, the edit in /boot/config.txt won't work**)
        ```
        sudo nano /boot/firmware/config.txt
        ```
    - Add the following line at the end
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
    - reboot the PI ```sudo reboot```
- After rebooting you can check `ls/dev` to see if you can see `ttySC0`, `ttySC1`, `ttySC2`, `ttySC3`.
    - ttySC0 is J8
    - ttySC1 is J7
    - ttySC2 is J4
    - ttySC3 is J5
    - ttySC4 is J9
    - ttySC5 is J10
    - ttySC6 is J14
    - ttySC7 is J15


- Testing the port with demo codes (provided by waveshare). **Or you can use minicom**
    - Download the code
    ```
    wget http://www.waveshare.com/w/upload/b/ba/Serial_Expansion_HAT_code.tar.gz
    tar zxvf Serial_Expansion_HAT_code.tar.gz
    sudo chmod 777 -R Serial_Expansion_HAT_code
    cd Serial_Expansion_HAT_code
    ```
    - test the code
    ```
    #Send data via Serial A
    cd c/uart/send
    make clean 
    make
    sudo ./uart_send
    ```
    ```
    #Receive data via Serial B
    cd c/uart/receive/
    make clean 
    make
    sudo ./uart_receive
    ```

## Test Xsens MTI-630
- On our Pi Hat (SBC_Hat_ Rise), we have a connector that allows us to directly interface with a MTI-630 AHRS. We have a [MTI ROS driver](https://github.com/GSO-soslab/xsens_mti_ros_driver/tree/7aa46b7f0a0576609062aaf46c518940e5fb4853) available for testing the communication and the board setup. The driver is a slightly modified version of the original MTI ROS driver.
- Port: `/dev/ttyS0` or `/dev/ttyAMA0`
- Default UART baudrate: `115200`
- Some [special setup](https://askubuntu.com/questions/1254376/enable-uart-communication-on-pi4-ubuntu-20-04) will be needed for Ubuntu 20.04 user since the raspi-config won't be able to enable the uart.
    - Back up the oroginal config.txt and cmdline.txt files 
    ```
    sudo cp -pr /boot/firmware/cmdline.txt /boot/firmware/cmdline.txt-orig
    sudo cp -pr /boot/firmware/config.txt /boot/firmware/config.txt-orig
    ```
    - Edit `/boot/firmware/config.txt` to comment out `enable_uart=1`
    ```
    #enable_uart=1
    cmdline=cmdline.txt
    ```
    - Remove the console setting `console=serial0,115200` from `/boot/firmware/cmdline.txt`
    - Disable serial service which used the miniUART
    ```
    sudo systemctl stop serial-getty@ttyS0.service
    sudo systemctl disable serial-getty@ttyS0.service
    sudo systemctl mask serial-getty@ttyS0.service
    ```
    - Add user to tty and dialout
    ```
    sudo adduser ${USER} tty
    sudo adduser ${USER} dialout
    ```
    - Reboot your pi
    - Someone also suggested to create a new file `/etc/udev/rules.d/10-local.rules`
    ```
    KERNEL=="ttyS0", SYMLINK+="serial0" GROUP="tty" MODE="0660"
    KERNEL=="ttyAMA0", SYMLINK+="serial1" GROUP="tty" MODE="0660"
    ```
    - Then, reload the udev rules: `sudo udevadm control --reload-rules && sudo udevadm trigger`
    - Add a newline `dtoverlay=disable-bt` to `/boot/firmware/config.txt` underneath `cmdline=cmdline.txt`
    - Worst case scenario, you can mount Xsense upside down and use a UART to USB bridge. This is the easiest fix.
- Disbale the u-boot interface with UART, check [reference](https://askubuntu.com/a/1287847)
    - Install the dependencies on your laptop for building new u-boot
    ```
    sudo apt install git make gcc gcc-aarch64-linux-gnu bison flex
    ```
    - Clone offical u-boot repository
    ```sh
    git clone --depth 1 git://git.denx.de/u-boot.git
    cd u-boot
    ```
    - Modify the *u-boot/configs/rpi_4_defconfig* by adding following lines in the end:
    ```
    CONFIG_BOOTDELAY=-2
    CONFIG_SILENT_CONSOLE=y
    CONFIG_SYS_DEVICE_NULLDEV=y
    CONFIG_SILENT_CONSOLE_UPDATE_ON_SET=y
    CONFIG_SILENT_U_BOOT_ONLY=y
    ```
    - Modify the *u-boot/include/configs/rpi.h* by adding following lines before `#endif`:
    ```c++
    #define CONFIG_EXTRA_ENV_SETTINGS \
    "dhcpuboot=usb start; dhcp u-boot.uimg; bootm\0" \
    "silent=1\0" \
    ENV_DEVICE_SETTINGS \
    ENV_DFU_SETTINGS \
    ENV_MEM_LAYOUT_SETTINGS \
    BOOTENV
    ```
    - Cross compile u-boot for Pi
    ```sh
    cd ~/path/u-boot
    make rpi_4_defconfig
    make CROSS_COMPILE=aarch64-linux-gnu-
    ```
    - Replace the kernal
        - rename the built *u-boot/u-boot.bin* to *uboot_rpi_4.bin*
        - backup the original file in your Pi such as */boot/firmware/uboot_rpi_4.bin.bak*
        - put the built file in your Pi inside */boot/firmware* folder

## Test ADC chip

## Follow the [instruction](http://wiki.ros.org/noetic/Installation/Ubuntu) to install ROS Noetic.
- You can install the base version
- the base version will take about 1 GB space

## Test Bar30 sensor from Blue Robotics
- Download the python testing code from Blue robotics [here](https://github.com/bluerobotics/ms5837-python)
- Install the library `pip install smbus2`

## GPIO control
On the hat we have 5 GPIOs (7,8, 9, 12, 13).
We use the GPIO as output pins to control MOSFET and power supplies to control sensor payloads.
GPIO9, 12, 13 can be configured as normal GPIO.

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
***Note***: For GPIO7 and GPIO8, they are originally used as chip select pin for SPI in the PI system. To free them to become a regular GPIO, you need to add the following line in `/boot/config.txt` and `/boot/firmware/config.txt` file after the line `dtparam=spi=off`. The added line will remapp the chip select pin to other GPIOs, i.e., 20 and 21 here.
Then, you can reboot the PI, and `GPIO7` and `GPIO8` can be used as normal GPIOs.
```
dtoverlay=spi0-cs,cs0_pin=20,cs1_pin=21
```


## Remote setup
The ubuntu we are using is server, to change the hostname, please refere to `/etc/cloud/templates/hosts.debian.tmpl`

## Make new image for Pi:
[reference](https://raspberrytips.com/create-image-sd-card/)
Notes: our image is available on request: please contact mzhou@uri.edu for more information.
- On Ubuntu:
    - check the Pi SDcard on ubuntu through the SD card reader:
    ```sh
    sudo fdisk -l
    ```
    - make new image based your system
    ```sh
    sudo dd bs=4M status=progress if=[device name] of=[image name]
    # Example
    # sudo dd bs=4M status=progress if=/dev/sde of=/your-path/vehicle-name_day_month_year.img
    ```
    - shrink image on Ubuntu:
    ```sh
    # dependency
    sudo apt-get install gparted
    # get shrink script
    wget https://raw.githubusercontent.com/GSO-soslab/PiShrink/master/pishrink.sh
    chmod +x pishrink.sh
    sudo mv pishrink.sh /usr/local/bin
    # usage
    cd /your-path
    cp your_file.img your_file_backup.img
    sudo pishrink.sh your_file.img
    ```
- On Windows: check the reference
- Verify:
    - check ADC: individually Bring up the Power Minotor in the `bringup_test.launch`
    - check AHRS: individually Bring up Xsens AHRS in the `bringup_test.launch`
    - check Pico: individually Bring up Pico MCU in the `bringup_test.launch`
 

## Time Synchronization

### Server side (Pi)

#### GPSD
gpsd is a linux software to parse the GPS NMEA strings and publish them.

- install dependency: `sudo apt install gpsd gpsd-clients pps-tools`
- copy the following to the file: `/etc/default/gpsd`
```sh
# Devices gpsd should collect to at boot time.
# They need to be read/writeable, either by user gpsd or the group dialout.

# Start at boot time
START_DAEMON="true"

USBAUTO="true"

DEVICES="/dev/ttyUSB0"

# Other options you want to pass to gpsd
GPSD_OPTIONS="-n"

BAUDRATE="9600"
```
- restart: `sudo systemctl restart gpsd`
- check the installation: `cgps -s`

#### Chrony
chrony is the linux software to time sync the system using different type of time sources (e.g., Inernet, GPS, other computer...)

- install dependency: `sudo apt install chrony`
- save the default file as backup 
- copy following to the file `/etc/chrony/chrony.conf`
```sh
### /etc/chrony/chrony.conf ###

#### This conf used for time sync from GPS 

## Internet server
pool ntp.ubuntu.com iburst maxsources 4

driftfile /var/lib/chrony/drift

# make it serve time even if it is not synced (as it can't reach out)
local stratum 10

## Used for NTP time sync for other system (e.g. DVL, Topside, Pi...)
allow 192.168.2.0/24
local stratum 8

## Used for time sync from gpsd daemon (NMEA string) 
makestep 1.0 3
maxupdateskew 100.0
refclock SHM 0 poll 2 refid GPS precision 1e-1 offset 0.128 trust
initstepslew 30
```
- restart: `sudo systemctl restart chrony.service`
- check: `watch -n -0.1 chronyc sources -v`

### Clinet side (Jetson)
- install dependency: `sudo apt install chrony`
- save the default file as backup
- copy following to the file `/etc/chrony/chrony.conf`: it comment out the Internet time server and set Pi as time server
```sh
# set the servers IP here to sync to it
## Internet server
#pool ntp.ubuntu.com iburst maxsources 4

## Set Pi as time server: could either use hostname or IP
Server raspberrypi minpoll 0 maxpoll 3

# This directive specify the location of the file containing ID/key pairs for
# NTP authentication.
keyfile /etc/chrony/chrony.keys

# This directive specify the file into which chronyd will store the rate
# information.
driftfile /var/lib/chrony/chrony.drift

# Uncomment the following line to turn logging on.
#log tracking measurements statistics

# Log files location.
logdir /var/log/chrony

# Stop bad estimates upsetting machine clock.
maxupdateskew 100.0

# This directive enables kernel synchronisation (every 11 minutes) of the
# real-time clock. Note that it can’t be used along with the 'rtcfile' directive.
rtcsync

# Step the system clock instead of slewing it if the adjustment is larger than
# one second, but only in the first three clock updates.
makestep 1 3

```
