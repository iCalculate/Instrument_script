# -*- coding: utf-8 -*-
"""
Demo for M336 and SMU2400 control
Du X.C., June 2023, Univ. of Electronic Science and Technology of China
"""
import time
import LakeShore
import Keithley
import StanfordResearch
import EXFO
import os
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
 
DevName = 'xxx-x-x'

Model336_GPIB_Addr = 12 # LakeShoreM336 Temperature controler GPIB address is 12
Keithley2400_GPIB_Addr = 3  # Keithley 2400 SourceMeter GPIB address is 3
Keithley2450_GPIB_Addr = 18  # Keithley 2400 SourceMeter GPIB address is 3
SR400_GPIB_Addr = 18  # Keithley 2400 SourceMeter GPIB address is 3
FVA3100_GPIB_Addr = 10  # FVA3100 variable attenuator GPIB address is 3
SR830_GPIB_Addr = 1  # SR830 Lock-in Amplifer GPIB address is 3
SR542_COM_Addr = 3      # SR542 Chopper serial port address is 1


# Initialization instrument interface
Md336 = LakeShore.Model335('GPIB0::' + str(Model336_GPIB_Addr) + '::INSTR')
SMU2400 = Keithley.Model2400('GPIB0::' + str(Keithley2400_GPIB_Addr) + '::INSTR')
SMU2450 = Keithley.Model2450('GPIB0::' + str(Keithley2450_GPIB_Addr) + '::INSTR')
SR400 = StanfordResearch.SR400('GPIB0::' + str(SR400_GPIB_Addr) + '::INSTR')
ATTEN = EXFO.FVA3100('GPIB0::' + str(FVA3100_GPIB_Addr) + '::INSTR')
Chopper = StanfordResearch.SR542('COM' + str(SR542_COM_Addr))


# LakeShore 335/336 code template
TempA = Md336.read_temperature(channel = 1)   # read sample(A) temperature
TempB = Md336.read_temperature(channel = 1)   # read rad shiedl(B) temperature
HeaterA = Md336.read_heater_value(channel = 1)    # read the A output heater value
HeaterB = Md336.read_heater_value(channel = 2)    # read the B output heater value

Md336.set_temperature(channel = 1, temp = 20)     # set channel A to 20K
Md336.set_heater_range(channel = 1, ranges = 2)   # set A output heater range 0,1,2,3 for Off,Low,Med,Hige

Md336.set_temp_stable(channel = 1, aim = 20, realtime=False )  # Set the temperature and wait until it stabilizes


# Keithley SMU code template
#---------Keithley 2450------------#
SMU2450.initSourceVolt(compCurr=1e-3)  # Initialize the voltage source and current complience
SMU2450.initSenseCurr(nplc=1)    # Initialize current sample and integration time form 0.01 to 10

dataVS = SMU2450.executeVoltSweep(top = 1, num = 20, loop = False ,polar = True)  # Voltage sweep form 0 to top with {num} point
dataVb = SMU2450.executeVoltBias(bias = 1, num = 20)  # Voltage bias at {bias} with {num} point
dataVbS = SMU2450.executeVoltBiasStep(start = 0, stop = 1, stepnum = 5, num = 10)

SMU2450.initSourceCurr(compVolt=1.0)   # Initialize the current source and voltage complience
SMU2450.initSenseVolt(nplc=1)    # Initialize voltage sample and integration time form 0.01 to 10

dataIS = SMU2450.executeCurrSweep(top = 1e-3, num = 20)   # Current sweep form 0 to top with {num} point
dataIb = SMU2450.executeCurrBias(bias = 1e-3, num = 20)   # Current bias at {bias} with {num} point
dataIbS = SMU2450.executeCurrBiasStep(start = 0, stop = 1e-3, stepnum = 5, num = 10)  
 

#---------Keithley 2400------------#
SMU2400.initSourceVolt()  # Initialize the voltage source
SMU2400.initSenseCurr(currComp = 0.01)   # Initialize current sample and current complience

dataVS = SMU2400.executeVoltSweep(top = 1, num = 20)
dataVb = SMU2400.executeVoltBias(bias = 1, num = 20)
dataVbS = SMU2400.executeVoltBiasStep(start = 0, stop = 1, stepnum = 6, num = 10)

SMU2400.initSourceCurr()  # Initialize the current source
SMU2400.initSenseVolt(voltComp = 1.0)   # Initialize current sample and voltage complience

dataIS = SMU2400.executeCurrSweep(top = 1e-3, num = 20)
dataIb = SMU2400.executeCurrBias(bias = 1e-3, num = 20)
dataIbS = SMU2400.executeCurrBiasStep(start = 0, stop = 1e-3, stepnum = 6, num = 10)


# Stanford Research SR400 code template
SR400.set_count_input(counter = 'A', source = 'INPUT1') # couple input1 to A port
SR400.set_disc_mode(channel = 1, fixed=True)   # set counter A with fixed disc mode
SR400.set_disc_level(channel = 'ch1', level = 2e-3, slope = True) # set counter A disc {level} and trigger mode {slope}
SR400.set_count_preset(channel = 'T', t = 0.5)  # set preset {channel} and preset time{t}
SR400.display_mode(conti=False)  # set display mode as finised and display
SR400.lcd_message(message = 'Test SR400...')  # Custom display
SR400.scan_end_mode(mode = 'STOP') # Stop counting while count finish
SR400.count_restart()
while(not SR400.check_count_finish()):  # wait for count finished
	countNum = SR400.read_last_count(channel = 'ch1')  # get last count number
	SR400.count_stop()
	
	
# Stanfrod Research SR542 code template
Chopper.inter_freq(freq = 50.0, query = False)  # set internal freq F = freq_internal*mult/divr
Chopper.mult(mult = 1)   # set multiplier
Chopper.divr(divr = 50)  # set divisor
Chopper.disp(mode = 0)   # Chopper Display the OUTER frequency
Chopper.on()   # Start chopper
time.sleep(10)
print("\tThe chopping freq = ", end='')
print(Chopper.read_freq(mode = 0), end='')  # read {mode} freqency 0 for outer freq
Chopper.off()  # Stop chopper


# FVA3100 Variable Attenuator code template
ATTEN.set_fiber(multimode=True)  # set attenuator fiber mode as multimode fiber
ATTEN.set_mode(absolute=True)   # set attenuator work at absolute mode
ATTEN.set_wavelength(wavelength=1550.0)  # set wavelength to 1550 nm
ATTEN.set_offset(offset=0.0)    # set offset to 0 dB
ATTEN.set_attenuation(atten=-20.0)  # set attenuation multiple to -20 dB
ATTEN.set_shutter(shutter=True)   # turn shutter ON


# close the GPIB communication interface
Md336.close()
SR400.close()
SMU2400.close()
SMU2450.close()
Chopper.close()
ATTEN.close()


# Data preservation code template
if not os.path.isdir(DevName): os.mkdir(DevName)  # Create a device name folder in the root path
	
curtime = time.strftime('%y-%m-%d_%H-%M-%S')
SavePath = os.path.join(DevName, f'{DevName}_XXXX_[{curtime}]' )
# save test data as ACSII text file
# SMU data format: [Volt, Curr, Resis, Time, Status]
np.savetxt(SavePath + '.txt', np.array(dataIS), fmt="%e", delimiter="\t",\
		   header="Voltage(V)\tCurrent(A)\tResistance(Ohm)\tStatus\tTime(s)")
# save test data as matlab data file 
scipy.io.savemat(SavePath +'.mat', \
				 mdict = {'volt':np.array(dataIS)[:,0], 'curr':np.array(dataIS)[:,1], \
					      'resis':np.array(dataIS)[:,2], 't':np.array(dataIS)[:,4]})
