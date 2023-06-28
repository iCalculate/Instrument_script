# -*- coding: utf-8 -*-
"""
Demo for M336 and SMU2400 control
Du X.C., June 2023, Univ. of Electronic Science and Technology of China
"""
import time
import datetime
import os
import scipy.io	   #to save .mat format data
from scipy.fftpack import fft
import LakeShore
import Keithley
import StanfordResearch
import numpy as np
import matplotlib.pyplot as plt
 
Model336_GPIB_Addr = 12 # LakeShoreM336 Temperature controler GPIB address is 12
Keithley2400_GPIB_Addr = 3  # Keithley 2400 SourceMeter GPIB address is 3
Keithley2450_GPIB_Addr = 18  # Keithley 2400 SourceMeter GPIB address is 3
SR542_COM_Addr = 3      # SR542 Chopper serial port address is 1

DevName = '419-4-x' # will be inserted into filename of saved plot
# Temp = 85

Md336 = LakeShore.Model335('GPIB0::' + str(Model336_GPIB_Addr) + '::INSTR')
SMU2400 = Keithley.Model2400('GPIB0::' + str(Keithley2400_GPIB_Addr) + '::INSTR')
SMU2450 = Keithley.Model2450('GPIB0::' + str(Keithley2450_GPIB_Addr) + '::INSTR')
Chopper = StanfordResearch.SR542('COM' + str(SR542_COM_Addr))

SMU2450.initSourceCurr(compVolt=2.0)
SMU2450.initSenseVolt(nplc=1.0)

for Temp in [10+i*1.0 for i in range(0,71)]:
	Md336.set_temp_stable(channel=1, aim=Temp, length=300, threshold=5e-5, tsample=1.0, realtime=False)
	
	'''
	IV sweep test and data save
	'''
	dataIS = SMU2450.executeCurrSweep(top=5e-3, num=500)

	vlist = np.array(dataIS)[:,0]
	Ic = dataIS[np.argmax(np.diff(vlist))][1]
	#Itop = (np.ceil(Ic*1000)+1)/1000
	Itop = (np.ceil(Ic*5e4)+1)/5e4  # find arround grid with 20uA step
	print(f'Ic at {Temp:.1f}K is {Ic*1e6:.2f}uA. Itop set at {Itop*1e6:.2f}uA')
	dataIS = SMU2450.executeCurrSweep(top=Itop, num=400)
	plt.plot(np.array(dataIS)[:,1],np.array(dataIS)[:,0])
	plt.show()
	
	
	if not os.path.isdir(DevName): os.mkdir(DevName)
	data = dataIS
	curtime = time.strftime('%y-%m-%d_%H-%M-%S')
	SavePath = os.path.join(DevName, f'{DevName}_Isweep_{Temp:.1f}K_[{curtime}]' )
	# save test data as ACSII text file
	scipy.io.savemat(SavePath +'.mat', \
	 				 mdict = {'volt':np.array(data)[:,0], 'curr':np.array(data)[:,1], \
	 					      'resis':np.array(data)[:,2], 't':np.array(data)[:,3]})
	
	'''
	Current bias step test and data save
	'''
	dataISb = SMU2450.executeCurrBiasStep(start=1.0e-6, stop=Itop, stepnum=41, num=200)
# 	dataISb = SMU2450.executeCurrBiasStep(start=0.30e-3, stop=0.34e-3, stepnum=10, num=200)	
	plt.plot(np.array(dataISb)[:,3],np.array(dataISb)[:,0])
	plt.show()
	
	if not os.path.isdir(DevName): os.mkdir(DevName)
	data = dataISb
	curtime = time.strftime('%y-%m-%d_%H-%M-%S')
	SavePath = os.path.join(DevName, f'{DevName}_CurrStep_{Temp:.1f}K_[{curtime}]' )
	# save test data as ACSII text file
	scipy.io.savemat(SavePath +'.mat', \
	 				 mdict = {'volt':np.array(data)[:,0], 'curr':np.array(data)[:,1], \
	 					      'resis':np.array(data)[:,2], 't':np.array(data)[:,3]})

	
# '''
# Current bias at step chopping freq
# '''
# dataIb = []
# divrList = [i*5 for i in list(range(1,21))]
# for divr in divrList:
#  	Chopper.divr(divr=divr)
#  	dataIb.extend(SMU2450.executeCurrBias(bias = 0.332e-3, num = 200))
 	
# bias = 0.3388e-3
# dataIb = SMU2450.executeCurrBias(bias = bias, num = 2000)
# plt.plot(np.array(dataIb)[:,3],np.array(dataIb)[:,0])
# plt.show()
# if not os.path.isdir(DevName): os.mkdir(DevName)
# data = dataIb
# curtime = time.strftime('%y-%m-%d_%H-%M-%S')
# SavePath = os.path.join(DevName, f'{DevName}_IBias{bias*1e6:.1f}uA_{Temp:.1f}K_[{curtime}]' )
# # save test data as ACSII text file
# scipy.io.savemat(SavePath +'.mat', \
#  				 mdict = {'volt':np.array(data)[:,0], 'curr':np.array(data)[:,1], \
#  					      'resis':np.array(data)[:,2], 't':np.array(data)[:,3]})




	
	