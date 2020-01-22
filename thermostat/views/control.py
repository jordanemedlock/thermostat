from flask import Blueprint, g, current_app, request, session
from thermostat.models import *
import glob

control = Blueprint('control', __name__)

@control.before_request
def initialize_variables():
  if current_app.config.get('NO_HARDWARE'):
    g.heater = MockHeater()
    g.cooler = MockCooler()
    g.thermometer = MockThermometer()
  else:
    g.heater = Heater(current_app.config.get('HEATER_PIN'))
    g.cooler = AC(current_app.config.get('COOLER_PIN'))
    g.thermometer = Thermometer()


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
  mode_file = current_app.config.get('MODE_FILE')
  if request.method=='POST':
    with open(mode_file, 'w') as fp:
      mode = mode.lower()
      if mode in ['off', 'heater', 'cooler', 'auto']:
        fp.write(mode)
    return mode
  else:
    with open(mode_file, 'r') as fp:
      mode = fp.read()
      print('mode', mode)
      return mode

@control.route('/temps', methods=['GET', 'POST'])
def temps():
  temps_file = current_app.config.get('TEMPS_FILE')
  if request.method == 'GET':
    with open(temps_file, 'rb') as fp:
      ts_string = fp.read()
      print(ts_string)
    return ts_string
  else:
    with open(temps_file, 'wb') as fp:
      temps = request.get_data()
      print(temps)
      fp.write(temps)
    return temps

