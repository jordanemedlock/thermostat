import sched
import time
import pickle
from models import *

data_file = 'thermostat.pkl'

scheduler = sched.scheduler(time.time, time.sleep)

heater = Heater(2)
cooler = MockCooler()
thermometer = Thermometer(14)
temp_range = TempRange(66,67,  78,80)
thermostat = Thermostat(heater, cooler, thermometer, temp_range, Thermostat.AUTO)

def run_thermostat(scheduler):
	print('running thermometer')

	thermostat.run_thermostat()

	scheduler.enter(60, 1, run_thermostat, (scheduler,))

run_thermostat(scheduler)
scheduler.run()
