# Info about supported Tools

Tools         | Vendor    | Version | Tcl | Comment
---           | ---       | ---     | --- | ---
ISE           | Xilinx    | 14.7    | 8.4 | Discontinued in 2013
Libero-SoC    | Microsemi | 12.2    | 8.5 | Important changes in version 12.0 (2019)
Quartus Prime | Intel     | 19.1    | 8.6 | Known as Quartus II until version 15.0 (2015)
Vivado        | Xilinx    | 2019.1  | 8.5 | It replaced ISE

Notes:
* ISE supports devices starting from Spartan 3/Virtex 4 until some first members of the 7 series.
Previous Spartan/Virtex devices were supported until version 10. Vivado supports devices starting
from the 7 series.
* Libero-SoC had a fork for PolarFire devices which was merged in version 12.0 (2019).
Libero SoC v12.0 and later supports PolarFire, RTG4, SmartFusion2 and IGLOO2 FPGA families.
Libero SoC v11.9 and earlier are the alternative to work with SmartFusion, IGLOO, ProASIC3 and
Fusion families.
Libero IDE v9.2 (2016) was the last version of the previous tool to work with antifuse and older
flash devices.
* Since the change from Quartus II to Prime, three editions are available: Pro (for Agilex,
Stratix 10, Arria 10 and Cyclone GX devices), Standard (for Cyclone 10 LP and earlier devices)
and Lite (a high-volume low-end subset of the Standard edition).
