import sched
import time
import json
from models import Thermostat, Thermometer

data_file = 'thermostat.json'

scheduler = sched.scheduler(time.time, time.sleep)
thermometer = Thermometer(14)
def run_thermostat(scheduler):
	with open('log.txt', 'a') as fp:
		try:
			with open(data_file, 'r') as fp:
				thermostat = Thermostat.from_json(json.load(fp), thermometer)

			thermostat.run_thermostat(fp)

			with open(data_file, 'w') as fp:
				json.dump(thermostat.to_json(), fp)
		except Exception as e:
			fp.write('error: {}'.format(e.msg))
			raise e

	scheduler.enter(60, 1, run_thermostat, (scheduler,))

run_thermostat(scheduler)
scheduler.run()
