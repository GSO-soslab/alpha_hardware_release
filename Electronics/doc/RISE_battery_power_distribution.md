
## **Battery power distribution board
This board is used to parallelize upto four battery packs to supply continuous energy for the ALPHA.

- Two rectifier diode arrays can be soldered (1 pair common cathode). We recommend to use `FERD60H100CGY-TR` which is rated at 100 V at 30A per diode. Or you can use `RB238NS150FHTLCT-ND` which is rated at 150v at 20A per diode.
- The diodes allows us to parallel multiple packs without charge each other. However, the downside is that only one battery pack (with the highest voltage) is supplying the energy to the overall system. Therefore, you need make sure the following things:
   - The battery's maximum discharge current rating is enough for your system
   - Your wiring for each battery is sufficient for carrying all the current.
- All the pads on the top layer are Positive pin of the battery or the output power. VB1 to VB4 pads are enlarged to allow two wires to be soldered on each pad. One wire connects to the battry, one wire connects to the charger.
- All the pads on the bottom layer are GND pads.