from flask import Blueprint, g, current_app, session
import threading
import requests



host = "localhost:5000"

def set(appliance, state):
  requests.post('http://{}/{}/{}'.format(host, appliance, state))

def off():
  set('heater', 'off')
  set('cooler', 'off')
def heat():
  set('heater', 'on')
  set('cooler', 'off')
def cool():
  set('heater', 'off')
  set('cooler', 'on')

def get_temp():
  return float(requests.get('http://{}/temperature'.format(host)).text)

def get_temps():
  ts_string = requests.get('http://{}/temps'.format(host)).text
  return list(map(float, ts_string.split(' ')))

def set_temps(*args):
  requests.post('http://{}/temps'.format(host), data=' '.join(args))

def get_mode():
  return requests.get('http://{}/mode'.format(host)).text


def run_thermostat(settings):
  global temp_range
  mode = get_mode()
  print('Mode: {}'.format(mode))
  if mode == 'off':
    off()
  if mode == 'heater':
    heat()
  if mode == 'cooler':
    cool()
  if mode == 'auto':
    f = get_temp()
    temp_range = get_temps()
    if f < temp_range[0]:
      print('Temperature: {} turning on heater'.format(f))
      heat()
    elif temp_range[1] < f < temp_range[2]:
      print('Temperature: {} turning off everything'.format(f))
      off()
    elif temp_range[3] < f:
      print('Temperature: {} turning on cooler'.format(f))
      cool()
    else:
      print('Temperature: {} not changing anything'.format(f))


def activate_thermostat(scheduler, settings):
  seconds = int(settings.get('THERMOSTAT_RUN_SECONDS'))
  scheduler.add_job(run_thermostat, trigger='interval', args=[settings], seconds=seconds)
