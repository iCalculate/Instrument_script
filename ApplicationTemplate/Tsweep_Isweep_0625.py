# -*- coding: utf-8 -*-
"""
Demo for M336 and SMU2400 control
Du X.C., June 2023, Univ. of Electronic Science and Technology of China
"""
import time
import os
import scipy.io	   #to save .mat format data
import LakeShore
import Keithley
import StanfordResearch
import numpy as np
import matplotlib.pyplot as plt
 
Model336_GPIB_Addr = 12 # LakeShoreM336 Temperature controler GPIB address is 12
Keithley2400_GPIB_Addr = 3  # Keithley 2400 SourceMeter GPIB address is 3
Keithley2450_GPIB_Addr = 18  # Keithley 2400 SourceMeter GPIB address is 3
SR542_COM_Addr = 3      # SR542 Chopper serial port address is 1

DevName = 'xxx-x-log' # will be inserted into filename of saved plot

Md336 = LakeShore.Model335('GPIB0::' + str(Model336_GPIB_Addr) + '::INSTR')
SMU2400 = Keithley.Model2400('GPIB0::' + str(Keithley2400_GPIB_Addr) + '::INSTR')
SMU2450 = Keithley.Model2450('GPIB0::' + str(Keithley2450_GPIB_Addr) + '::INSTR')
Chopper = StanfordResearch.SR542('COM' + str(SR542_COM_Addr))

SMU2450.initSourceCurr(compVolt=5.0)
SMU2450.initSenseVolt(nplc=1)


Tlist = [45+i*0.5 for i in range(61)]

for temp in Tlist:
	
	Md336.set_heater_range(channel = 1, ranges = 3)   #Set the heater of channel 1 as high(3) range
	Md336.set_temp_stable(channel = 1, aim = temp, length = 500, threshold = 1e-4, tsample = 0.1, realtime=False)
	
	SMU2450.initSourceCurr(compVolt=2.0)
	SMU2450.initSenseVolt(nplc=1)
	
	dataIS = SMU2450.executeCurrLogSweep(start = 1e-8, stop = 2.0e-3, num = 300)  # I sweep from 0 top 
	#dataIS = SMU2450.executeCurrSweep(top = 2.0e-3, num = 300)  # I sweep from 0 top 
	plt.plot(np.array(dataIS)[:,1],np.array(dataIS)[:,0], color = 'tab:blue', linestyle = '-', marker = ',')
	plt.show()
	
	if not os.path.isdir(DevName): os.mkdir(DevName)
	
	curtime = time.strftime('%y-%m-%d_%H-%M-%S')
	SavePath = os.path.join(DevName, f'{DevName}_Isweep_{temp:.3f}K_[{curtime}]' )
	# save test data as ACSII text file
	np.savetxt(SavePath + '.txt', np.array(dataIS), fmt="%e", delimiter="\t",\
			   header="Voltage(V)\tCurrent(A)\tResistance(Ohm)\tTime(s)")
	scipy.io.savemat(SavePath +'.mat', \
					 mdict = {'volt':np.array(dataIS)[:,0], 'curr':np.array(dataIS)[:,1], \
						      'resis':np.array(dataIS)[:,2], 't':np.array(dataIS)[:,3]})
