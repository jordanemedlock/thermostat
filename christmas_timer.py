import time
# from RPi.GPIO import *
import apscheduler.schedulers.blocking

# setmode(BCM)

# setup(2,OUT)

def turn_on():
	print('low')
    # output(2,LOW)

def turn_off():
	print('high')
    # output(2,HIGH)

sched = apscheduler.schedulers.blocking.BlockingScheduler()
sched.add_job(turn_on, 'cron', minute='30')
sched.add_job(turn_off, 'cron', minute='45')
sched.start()