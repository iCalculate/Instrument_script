# -*- coding: utf-8 -*-
"""
Demo for M336 and SMU2400 control
Du X.C., June 2023, Univ. of Electronic Science and Technology of China
"""
import time
import LakeShoreM335
import Keithley
import ModelSR542
import numpy as np
import matplotlib.pyplot as plt
 
Model336_GPIB_Addr = 12 # LakeShoreM336 Temperature controler GPIB address is 12
Keithley2400_GPIB_Addr = 3  # Keithley 2400 SourceMeter GPIB address is 3
Keithley2450_GPIB_Addr = 18  # Keithley 2400 SourceMeter GPIB address is 3
SR542_COM_Addr = 3      # SR542 Chopper serial port address is 1

# Initialization instrument interface
Md336 = LakeShoreM335.Model335('GPIB0::' + str(Model336_GPIB_Addr) + '::INSTR')
SMU2400 = Keithley.Model2400('GPIB0::' + str(Keithley2400_GPIB_Addr) + '::INSTR')
SMU2450 = Keithley.Model2450('GPIB0::' + str(Keithley2450_GPIB_Addr) + '::INSTR')
Chopper = ModelSR542.SR542('COM' + str(SR542_COM_Addr))


TempA = Md336.read_temperature(channel = 1)   # read sample(A) temperature
TempB = Md336.read_temperature(channel = 1)   # read rad shiedl(B) temperature

SMU2450.initSourceVolt(compCurr=1e-3)
SMU2450.initSenseCurr(nplc=1)

dataVS = SMU2450.executeVoltSweep(top = 1, num = 20, loop = False ,polar = True)
plt.plot(np.array(dataVS)[:,3],np.array(dataVS)[:,1])
plt.show()
dataVb = SMU2450.executeVoltBias(bias = 1, num = 20)
plt.plot(np.array(dataVb)[:,3],np.array(dataVb)[:,1])
plt.show()
dataVbS = SMU2450.executeVoltBiasStep(start = 0, stop = 1, stepnum = 5, num = 10)
plt.plot(np.array(dataVbS)[:,3],np.array(dataVbS)[:,1])
plt.show()

SMU2450.initSourceCurr(compVolt=1.0)
SMU2450.initSenseVolt(nplc=1)

dataIS = SMU2450.executeCurrSweep(top = 1e-3, num = 20)
dataIb = SMU2450.executeCurrBias(bias = 1e-3, num = 20)
dataIbS = SMU2450.executeCurrBiasStep(start = 0, stop = 1e-3, stepnum = 5, num = 10)


Md336.set_heater_range(channel = 1, ranges = 3)   #Set the heater of channel 1 as medium(3) range
Md336.set_temperature(1, 295)   #set the temperature of channel 1 as 40K
Md336.set_temp_stable(channel = 1, aim = 10, length = 60, threshold = 1, tsample = 0.1)

Chopper.inter_freq(freq = 50.0, query = False)
Chopper.mult(mult = 1)
Chopper.divr(divr = 50)
Chopper.disp(mode = 0)   # Chopper Display the OUTER frequency
Chopper.on()
time.sleep(10)
print("\tThe chopping freq = ", end='')
print(Chopper.read_freq(mode = 0), end='')  #OUTER
Chopper.off()

SMU2400.initSourceVolt()
SMU2400.initSenseCurr(currComp = 0.01)

dataVS = SMU2400.executeVoltSweep(top = 1, num = 20)
dataVb = SMU2400.executeVoltBias(bias = 1, num = 20)
dataVbS = SMU2400.executeVoltBiasStep(start = 0, stop = 1, stepnum = 6, num = 10)

SMU2400.initSourceCurr()
SMU2400.initSenseVolt(voltComp = 1.0)

dataIS = SMU2400.executeCurrSweep(top = 1e-3, num = 20)
dataIb = SMU2400.executeCurrBias(bias = 1e-3, num = 20)
dataIbS = SMU2400.executeCurrBiasStep(start = 0, stop = 1e-3, stepnum = 6, num = 10)

Md336.set_heater_range(channel = 1, ranges = 0)

Md336.close()
SMU2400.close()
Chopper.close()

