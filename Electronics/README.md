# ALPHA Hardware Repositority

## **Introduction**
This repository includes PCB designed for the ALPHA AUV

The most recent update:
- `sbc_hat_v2` is in production. Small mistakes have been corrected.
- `sbc_hat_RISE` is in production. This a simplier version converted from sbc_hat_v2. There are two big changes: 1) removed the MCU and 2) Xsens is directly mounted on the board.
- `thruster_driver` is in production. This is a breakout board for MCU (MicroMod RP2040). This board is designed for interface with ESCs to control the thruster and servos. The voltage sensing capability is available (using a voltage devider) to monitoring the voltage to the thrusters. Communication ports are I2C, RS232 and RS485. Two additional GPIO is available for Digital Output fucntion.
 

The hardware information is available in the following links
- [PI setup guide](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/PI_setup_guide.md) (Active)

- [`sbc_hat_rise`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/SBC_HAT_RISE.md) (Active)

- [`sbc_hat_rise_no_usb`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/SBC_HAT_RISE_no_usb.md) (Active)

- [`thruster_driver`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/Thruster_driver.md) (Active)

- [`alpha_power_distribution_board`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/Alpha_power_distribution.md) (Active)

- [`alpha_relay_management`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/Alpha_relay_management.md) (Active)

- [`RISE_battery_power_distribution`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/RISE_battery_power_distribution.md) (Active)

- [Mast_interface]() (Active)

- [`sb_hat_v2`](https://github.com/GSO-soslab/alpha_hardware/blob/master/doc/Boards/SBC%20HAT%20V2.md) (Not active)