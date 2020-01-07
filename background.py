import sched
import time
import pickle
from models import Thermostat

data_file = 'thermostat.pkl'

scheduler = sched.scheduler(time.time, time.sleep)

def run_thermostat(scheduler):
	print('doing stuff')

	with open(data_file, 'rb') as fp:
		thermostat = pickle.load(fp)

	thermostat.run_thermostat()

	with open(data_file, 'wb') as fp:
		pickle.dump(thermostat, fp)


	scheduler.enter(60, 1, run_thermostat, (scheduler,))

run_thermostat(scheduler)
scheduler.run()
