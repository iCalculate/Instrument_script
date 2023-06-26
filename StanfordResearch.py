# -*- coding: utf-8 -*-
"""
LakeShore Model335/336 comm. lib.
Du X.C., June 2023, Univ. of Electronic Science and Technology of China
Installed PyVISA for GPIB communication.
"""

import serial
import datetime
import time

class SR542 (object):
	def __init__(self, com_name, timeout:float = 0.5):
		
		self.ser = serial.Serial(port = com_name,
							baudrate = 115200,
							bytesize = serial.EIGHTBITS,
							parity = serial.PARITY_NONE,
							stopbits = serial.STOPBITS_ONE,
							timeout = 0.5) 
		print(com_name+' ->')
		self.ser.write("*IDN?\r\n".encode('utf-8'))
		idn = self.ser.readline()
		print(idn.decode())
		
	def write(self, string:str):
		string_term = string + "\r\n"
		self.ser.write(string_term.encode('utf-8'))
		
	def read(self):
		msg = self.ser.readline()
		return msg.decode('utf-8')

	def query(self, string:str):
		self.write(string)
		return self.read()
	
	def close(self):
		self.ser.close()
	
	def on(self):
		self.write("MOTR ON")
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Chopper ON.')
		
	def off(self):
		self.write("MOTR OFF")
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Chopper OFF.')
	
	def mult(self, mult:int, query = False):
		if query:
			return self.query("MULT?")
		elif 1<=mult<=200:
			self.write("MULT "+str(mult))
		else:
			print("The chopper mult number must in [1, 200]")
	
	def divr(self, divr:int, query = False):
		if query:
			return self.query("DIVR?")
		elif 1<=divr<=200:
			self.write("DIVR "+str(divr))
		else:
			print("The chopper mult number must in [1, 200]")
			
	def disp(self, mode:int, query = False):
		if query:
			return self.query("DISP?")
		elif 0 <= mode <= 8:
			self.write("DISP "+str(mode))
		else:
			print("Incorrect display mode index")
	
	def read_freq(self, mode:int):
		if 0 <= mode <= 6:
			return self.query("MFRQ? "+str(mode))
		else:
			print("Incorrect freq_monitor mode index")
			
	def inter_freq(self, freq:float = 100, query = True):
		if query:
			return self.query("IFRQ?")
		elif 1.0<=freq<=1000.0:
			self.write(f"IFRQ {freq:.3f}")
		else:
			print("Illegal internal frequency value")
	
	