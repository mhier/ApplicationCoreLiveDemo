#!/usr/bin/python3

import deviceaccess as da
import sys
import numpy as np

da.setDMapFilePath("devices.dmap")

dev = da.Device("MyAMC")
dev.open()

dev.write("BSP.CLK_MUX", [0, 1, 2, 3])  
    
clock_freq = dev.read("BSP.CLK_FREQ", dtype=np.uint32)
if clock_freq[0] != 125000000:
    print(f"Incorrect clock frequency detected: {clock_freq[0]}")
    sys.exit(1)

print(f"Correct clock frequency detected: {clock_freq[0]}")
print("Device successfully initialised.")