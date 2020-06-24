from iotgpio import Relay, DS18B20
import time


class Heater(Relay):
  pass

class AC:
  def __init__(self, compressor_pin, high_pin, low_pin):
    self.compressor = Relay(compressor_pin)
    self.high = Relay(high_pin)
    self.low = Relay(low_pin)
  
  def on(self, high=True):
    self.low.off()
    self.high.on()
    self.compressor.on()
  
  def off(self):
    self.low.off()
    self.high.off()
    self.compressor.off()
  
  @property
  def is_on(self):
    return self.compressor.is_on

class MockHeater():
  def on(self):
    pass

  def off(self):
    pass

  @property
  def is_on(self):
    return False
  

class MockCooler():
  def on(self, high=True):
    pass

  def off(self):
    pass

  @property
  def is_on(self):
    return False

class MockThermometer():
  @property
  def celcius(self):
    return 20
  
  @property
  def fahrenheit(self):
    return self.celcius * 9 / 5 + 32
  
  

class Thermometer(DS18B20):
  pass

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

  def run_thermostat(self, log):
    log.write('running thermostat with mode: {}'.format(self.mode))
    if self.mode == self.AUTO:
      
      f = self.thermometer.fahrenheit

      if f <= self.temp_range.lowest:
        log.write('temp too low turning up the heat {} <= {}'.format(f, self.temp_range.lowest))
        self.heat()
      elif self.temp_range.lower < f < self.temp_range.upper:
        log.write('leaving it there {} < {} < {}'.format(self.temp_range.lower, f, self.temp_range.upper))
        self.off()
      elif self.temp_range.uppest < f:
        log.write('temp too high turning up the ac {} > {}'.format(f, self.temp_range.uppest))
        self.cool()
      else:
        log.write('intermediate area, leaving same {}*F'.format(f))
    elif self.mode == self.HEATER:
      self.heat()
    elif self.mode == self.COOLER:
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
  
  
