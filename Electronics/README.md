# ALPHA Hardware Repositority

The ALPHA Eletronics Hardware design is released under  [CERN-OHL-S-2.0](https://ohwr.org/cern_ohl_s_v2.txt) Licence
## **Introduction**

The most recent update:

- `sbc_hat` is a expansion board for single-board computers. It contains 8 RS232 ports (4 selectable between UART and RS232), 2 I2C buses, 2 ADC channels, and 5 direct GPIO connections


- `thruster_driver` is a breakout board for MCU (MicroMod RP2040). This board is designed for interface with ESCs to control the thruster and servos. The voltage sensing capability is available (using a voltage devider) to monitoring the voltage to the thrusters. Communication ports are I2C, RS232 and RS485. Two additional GPIO is available for Digital Output fucntion.
 
- `Battery management` is a breakout board that uses diodes to allow battery pack parallization upto 4 packs. **IMPORTANT: You cannot charge batter packs from the Vout port on the board**

- `alpha_power_distribution_board` is a breakout board for distributing power sources for different devices on the ALPHA. You can plug in Pololu DC/DC circuit on the board with a 90 degree angled pin headers. 

The detailed hardware information is available in the following links for users.
- [PI setup guide](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/PI_setup_guide.md): This document provide information on how to configure the chips on the sbc_hat PBC.

- [`sbc_hat_rise`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/SBC_HAT_RISE.md) (Active)

- [`sbc_hat_rise_no_usb`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/SBC_HAT_RISE_no_usb.md) (Active)

- [`thruster_driver`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/Thruster_driver.md) (Active)

- [`alpha_power_distribution_board`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/Alpha_power_distribution.md) (Active)

- [`alpha_relay_management`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/Alpha_relay_management.md) (Active)

- [`RISE_battery_power_distribution`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/RISE_battery_power_distribution.md) (Active)

- [Mast_interface]() (Active)

- [`sb_hat_v2`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/SBC%20HAT%20V2.md) (Not active)