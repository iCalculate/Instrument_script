# -*- coding: utf-8 -*-
"""
EXFO comm. lib.
Du X.C., June 2023, Univ. of Electronic Science and Technology of China
Installed PyVISA for GPIB communication.
"""

import pyvisa
# import time
# import warnings
# import datetime

class FVA3100(object):
	def __init__(self, visa_name, timeout:int = 5000):
		rm = pyvisa.ResourceManager()
		self.pyvisa = rm.open_resource(visa_name)
		self.pyvisa.timeout = timeout # Wait for instrument return value, default is infinite wait
		print(visa_name+' ->')
		print(self.pyvisa.query("*IDN?"))
		
	def read(self):
		return self.pyvisa.read()

	def write(self, string):
		self.pyvisa.write(string)

	def query(self, str):
		return self.pyvisa.query(str)
    
	def close(self):
		return self.pyvisa.close()
	
	def set_attenuation(self, atten = -20, query:bool= False):
		'''
		This command sets the attenuation to a specific value. The valid range of values depends on the configuration of the FVA-3100 and on the current wavelength. The resolution of the value is 0.005 dB for singlemode models and 0.01 dB for multimode models.
		:param atten: actual attenuation value, defaults to -20
		:type atten: float, optional
		:param query: True for query attenuation value, defaults to False
		:type query: bool, optional
		:return: attenuation value
		:rtype: str

		'''
		if query:
			return self.query('ATT?')
		else:
			self.write(f'ATT {atten:.3f} DB')
	
	def set_offset(self, offset = 0.0, query:bool = False):
		'''
		This command stores an offset value that will be applied to all wavelengths in Absolute, Reference, and Offset modes. This offset value will be included in the measurement returned by ATT? but will not be taken into account on the FVA-3100 display. This offset value is deleted when the FVA-3100 is turned off.
		:param offset: offset value, defaults to 0.0
		:type offset: float, optional
		:param query: True for query offset value, defaults to False
		:type query: bool, optional
		:return: offset value
		:rtype: str

		'''
		if query:
			return self.query('CAL?')
		else:
			self.write(f'CAL {offset:.3f} DB')
			
	def set_shutter(self, shutter:bool = False, query:bool = False):
		'''
		This command controls the shutter, which can block optical continuity
		:param shutter: True for ON False for OFF, defaults to False
		:type shutter: bool, optional
		:param query: True for shutter status query, defaults to False
		:type query: bool, optional
		:return: shutter status
		:rtype: bool
		
		'''
		if query:
			return bool(int(self.query('D?')))
		else:
			self.write(f'D {str(int(shutter))}')
	
	def set_fiber(self, multimode:bool = True, query:bool = False):
		'''
		This command specifies the type of fiber tested (singlemode or multimode).
		:param multimode: True for multimode False for singlemode, defaults to True
		:type multimode: bool, optional
		:param query: True for query, defaults to False
		:type query: bool, optional
		:return: fiber mode
		:rtype: bool

		'''
		if query:
			return bool(int(self.query('F?'))-1)
		else:
			self.write(f'F {str(int(multimode)+1)}')
			
	def set_wavelength(self, wavelength = 1550.0, query:bool = False):
		'''
		
		:param wavelength: The <numeric_value> parameter is the actual wavelength in the format “9999.9 NM”. The units are optional, defaults to 1550.0
		:type wavelength: float, optional
		:param query: True for wavelength query, defaults to False
		:type query: bool, optional
		:return: wavelength
		:rtype: str

		'''
		if query:
			return self.query('INP:WAVE??')
		else:
			self.write(f'INP:WAVE {wavelength:.1f} NM')
			
	def set_mode(self, absolute:bool = True, query:bool = False):
		'''
		This command selects Absolute or Reference attenuation mode. When Absolute mode is selected, the Absolute attenuation introduced by the FVA-3100 is displayed. When Reference mode is selected, the current absolute attenuation is set as the reference value, and then the displayed attenuation is relative to the reference.
		:param absolute: True for absolute False for Reference, defaults to True
		:type absolute: bool, optional
		:param query: True for mode query, defaults to False
		:type query: bool, optional
		:return: Absolute or Reference attenuation mode.
		:rtype: bool

		'''
		if query:
			return bool(int(self.query('OUTP:APM?')))
		else:
			self.write(f'OUTP:APM {str(int(absolute))}')