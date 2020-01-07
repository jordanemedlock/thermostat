from iotgpio import *


class Heater(Relay):
	pass

class AC(Relay):
	pass

class MockCooler():
	def on(self):
		pass
	def off(self):
		pass

class Thermometer(DHT11):
	@property
	def celsius(self):
		return self.temperature

	@property
	def fahrenheit(self):
		return int(self.temperature * (9/5) + 32)

class TempRange(object):
	def __init__(self, lowest, lower, upper, uppest):
		self.lower = lower
		self.lowest = lowest
		self.upper = upper
		self.uppest = uppest

	
class Thermostat(object):
	HEATER = 'heater'
	COOLER = 'cooler'
	AUTO = 'auto'
	OFF = 'off'
	def __init__(self, heater, cooler, thermometer, temp_range, mode):
		self.heater = heater
		self.cooler = MockCooler()
		self.thermometer = thermometer
		self.temp_range = temp_range
		self.mode = mode

	def set_mode(self, mode):
		self.mode = mode
		if mode == self.HEATER:
			self.heat()
		elif mode == self.COOLER:
			self.cool()
		elif mode == self.OFF:
			self.off()
		elif mode == self.AUTO:
			self.run_thermostat()

	def heat(self):
		self.cooler.off()
		self.heater.on()

	def cool(self):
		self.heater.off()
		self.cooler.on()

	def off(self):
		self.heater.off()
		self.cooler.off()

	def run_thermostat(self):
		print('running thermostat with mode: {}'.format(self.mode))
		if self.mode != self.AUTO:
			return None

		if self.thermometer.fahrenheit < self.temp_range.lowest:
			print('temp too low turning up the heat {} < {}'.format(self.thermometer.fahrenheit, self.temp_range.lowest))
			self.heat()
		elif self.temp_range.lower < self.thermometer.fahrenheit < self.temp_range.upper:
			self.off()
		elif self.temp_range.uppest < self.thermometer.fahrenheit:
			print('temp too high turning up the ac {} > {}'.format(self.thermometer.fahrenheit, self.temp_range.uppest))
			self.cool()

	@property
	def temperature(self):
		return self.thermometer.fahrenheit

	@property
	def is_heater_on(self):
		return self.heater.is_on

	@property
	def is_cooler_on(self):
		return self.cooler.is_on
	
	def to_json(self):
		return 
	
	

