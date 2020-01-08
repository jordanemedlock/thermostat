from iotgpio import *


class Heater(Relay):
	def to_json(self):
		return {
			'channel': self.channel,
			'state': self.state
		}
	@classmethod
	def from_json(cls, obj):
		channel = obj.get('channel', None)
		state = obj.get('state', None)
		if channel != None and state != None:
			self = cls(channel)
			self.state = state
			return self
		else:
			return None

class AC(Relay):
	def to_json(self):
		return {
			'channel': self.channel,
			'state': self.state
		}
	@classmethod
	def from_json(cls, obj):
		channel = obj.get('channel', None)
		state = obj.get('state', None)
		if channel != None and state != None:
			self = cls(channel)
			self.state = state
			return self
		else:
			return None

class MockCooler():
	def on(self):
		pass
	def off(self):
		pass
	@property
	def is_on(self):
		return False
	def to_json(self):
		return {}
	@classmethod
	def from_json(cls, obj):
		return cls()

class Thermometer(DHT11):
	@property
	def celsius(self):
		return self.temperature

	@property
	def fahrenheit(self):
		return int(self.temperature * (9/5) + 32)

	def to_json(self):
		return {
			'channel': self.channel
		}

	@classmethod
	def from_json(cls, obj):
		channel = obj.get('channel', None)
		if channel != None:
			return cls(channel)
		else:
			return None

class TempRange(object):
	def __init__(self, lowest, lower, upper, uppest):
		self.lower = lower
		self.lowest = lowest
		self.upper = upper
		self.uppest = uppest

	def to_json(self):
		return [self.lowest, self.lower, self.upper, self.uppest]

	@classmethod
	def from_json(cls, obj):
		if len(obj) == 4:
			return cls(*obj)
		else:
			return None

	
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

		f = None
		seconds = 0
		while not f and seconds < 5:
			try:
				f = self.thermometer.fahrenheit
			except RuntimeError as e:
				time.sleep(1)
				seconds += 1
		if not f:
			raise e


		if f < self.temp_range.lowest:
			print('temp too low turning up the heat {} < {}'.format(f, self.temp_range.lowest))
			self.heat()
		elif self.temp_range.lower < f < self.temp_range.upper:
			print('leaving it there {} < {} < {}'.format(self.temp_range.lower, f, self.temp_range.upper))
			self.off()
		elif self.temp_range.uppest < f:
			print('temp too high turning up the ac {} > {}'.format(f, self.temp_range.uppest))
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
		return {
			'mode': self.mode,
			'heater': self.heater.to_json(),
			'cooler': self.cooler.to_json(),
			'thermometer': self.thermometer.to_json(),
			'temp_range': self.temp_range.to_json()
		}

	@classmethod
	def from_json(cls, obj):
		mode = obj.get('mode', None)
		heater = Heater.from_json(obj['heater'])
		cooler = MockCooler.from_json(obj['cooler'])
		thermometer = Thermometer.from_json(obj['thermometer'])
		temp_range = TempRange.from_json(obj['temp_range'])
		if mode and heater and cooler and thermometer and temp_range:
			return cls(heater, cooler, thermometer, temp_range, mode)
		else:
			print(mode, heater, cooler, thermometer, temp_range)
			return None
	
	
