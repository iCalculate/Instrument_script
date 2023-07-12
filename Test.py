# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:50:06 2023

@author: iCalculate
"""

# -*- coding: utf-8 -*-
"""
Demo for M336 and SMU2400 control
Du X.C., June 2023, Univ. of Electronic Science and Technology of China
"""
import time
# import LakeShore
# import Keithley
import StanfordResearch
# import EXFO
# import os
# import scipy.io
# import numpy as np
# import matplotlib.pyplot as plt
 
DevName = 'xxx-x-x'

# Model336_GPIB_Addr = 12 # LakeShoreM336 Temperature controler GPIB address is 12
# Keithley2400_GPIB_Addr = 3  # Keithley 2400 SourceMeter GPIB address is 3
# Keithley2450_GPIB_Addr = 18  # Keithley 2400 SourceMeter GPIB address is 3
# SR400_GPIB_Addr = 18  # Keithley 2400 SourceMeter GPIB address is 3
# FVA3100_GPIB_Addr = 10  # FVA3100 variable attenuator GPIB address is 3
SR830_GPIB_Addr = 1  # SR830 Lock-in Amplifer GPIB address is 3
# SR542_COM_Addr = 3      # SR542 Chopper serial port address is 1



# Initialization instrument interface
# Md336 = LakeShore.Model335('GPIB0::' + str(Model336_GPIB_Addr) + '::INSTR')
# SMU2400 = Keithley.Model2400('GPIB0::' + str(Keithley2400_GPIB_Addr) + '::INSTR')
# SMU2450 = Keithley.Model2450('GPIB0::' + str(Keithley2450_GPIB_Addr) + '::INSTR')
# SR400 = StanfordResearch.SR400('GPIB0::' + str(SR400_GPIB_Addr) + '::INSTR')
# ATTEN = EXFO.FVA3100('GPIB0::' + str(FVA3100_GPIB_Addr) + '::INSTR')
# Chopper = StanfordResearch.SR542('COM' + str(SR542_COM_Addr))
SR830 = StanfordResearch.SR830('GPIB0::' + str(SR830_GPIB_Addr) + '::INSTR')

# SR830.set_sens_sensitivity(sensitivity=21)
SR830.set_sens_lpfslope(slope=0)
# SR830.set_sens_timeconstant(time_const=6)
SR830.set_sens_synchronous(status=False)
# SR830.set_sens_synchronous(status=True)

# SR830.set_ref_freq(freq=1000.0)
SR830.set_ref_phase(phase=0.0)
SR830.set_ref_mode(inter=True)


SR830.set_buffer_rate(rate=4)
SR830.set_buffer_start()
time.sleep(10.5)
SR830.set_buffer_pause()
print(SR830.read_buffer_data(buffer=1, start=0, num=10))

# # freqList = [-2+0.1*i-2 for i in range(200)]
# freqList = [pow(10,0.01*i-1) for i in range(331)]
# for i in freqList:
# 	SR830.set_ref_freq(freq = i)
# 	print(SR830.read_R())
# 	time.sleep(1/i*4)


# SR830.close()
