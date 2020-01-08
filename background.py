import sched
import time
import pickle
from models import Thermostat

data_file = 'thermostat.pkl'

scheduler = sched.scheduler(time.time, time.sleep)

def run_thermostat(scheduler):
	print('doing stuff')

	thermostat.run_thermostat()

	scheduler.enter(60, 1, run_thermostat, (scheduler,))

run_thermostat(scheduler)
scheduler.run()
