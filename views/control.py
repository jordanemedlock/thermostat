from flask import Blueprint, g, current_app, request, session
from models import *
import glob

control = Blueprint('control', __name__)

@control.before_request
def initialize_variables():
  g.heater = Heater(2)
  g.cooler = AC(3)
  g.thermometer = Thermometer()
  if 'mode' not in session:
    session['mode'] = 'off'


@control.route('/cooler', methods=['GET'], defaults={'on_off':None})
@control.route('/cooler/<on_off>', methods=['POST'])
def cooler_set(on_off):
  if request.method=='POST':
    if on_off.lower() == 'on':
      g.cooler.on()
      return 'on'
    elif on_off.lower() == 'off':
      g.cooler.off()
      return 'off'
  else:
    return 'on' if g.cooler.is_on else 'off'


@control.route('/heater', methods=['GET'], defaults={'on_off': None})
@control.route('/heater/<on_off>', methods=['POST'])
def heater_set(on_off):
  if request.method in ['POST']:
    if on_off.lower() == 'on':
      g.heater.on()
      return 'on'
    elif on_off.lower() == 'off':
      g.heater.off()
      return 'off'
  else:
    return 'on' if g.heater.is_on else 'off'


@control.route('/temperature/', methods=['GET'])
def temperature():
  return str(g.thermometer.fahrenheit)

@control.route('/mode', methods=['GET'], defaults={'mode': None})
@control.route('/mode/<mode>', methods=['POST'])
def mode(mode):
  if request.method=='POST':
    with open('mode.txt', 'w') as fp:
        mode = mode.lower()
        if mode in ['off', 'heater', 'cooler', 'auto']:
            fp.write(mode)
    return mode
  else:
    with open('mode.txt', 'r') as fp:
        return fp.read()

@control.route('/temps', methods=['GET', 'POST'])
def temps():
  if request.method == 'GET':
    with open('temps.txt', 'rb') as fp:
      ts_string = fp.read()
      print(ts_string)
    return ts_string
  else:
    with open('temps.txt', 'wb') as fp:
      temps = request.get_data()
      print(temps)
      fp.write(temps)
    return temps

