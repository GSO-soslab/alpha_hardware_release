
## **ALPHA Power distribution board**

This board is designed to distribute the input voltage for different systems on the ALPHA AUV.
- The terminal blocks are rated at 16A. This is good for thrusters, input battery lines, and other high current draw sensors.
- The JST-XH connector are rated at 3A. This is designed for mid-low power sensors. 
- There are several JST-XH outputs 5v and 12v as indicated on the board. 
   - `5V3`, `5V2` and `5V1` obtains 5V power from different `D36V28F5` DC/DC regulator (5-50v input range with a max current rating of 3.2A) 
   - `12v` ports obtain power from a `D36V50F12` (5-50v input range with a maximum current rating of 4.5A)
   - Qwiic connector pins are connected to the enable pin of the `D36V50F12`, `D36V28F5`. 
      - Pin 1 controls 5V1 from U1
      - Pin 2 controls 5V2 from U2
      - Pin 3 controls 5V3 from U3
      - Pin 4 controls 12V from U4
