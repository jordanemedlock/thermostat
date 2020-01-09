from flask import Blueprint, g, current_app, request, session
from models import *
import glob

control = Blueprint('control', __name__)


def get_device_file():
  base_dir = '/sys/bus/w1/devices/'
  # device_folder = glob.glob(base_dir + '28*')[0]
  # device_folder = 
  device_file = device_folder + '/w1_slave'
  return device_file

@control.before_request
def initialize_variables():
  g.heater = Heater(2)
  g.cooler = AC(3)
  #g.thermometer = Thermometer(get_device_file())
  if 'mode' not in session:
    session['mode'] = 'off'


@control.route('/cooler/<on_off>', methods=['GET', 'POST'])
def cooler_set(on_off):
  if request.method=='POST':
    if on_off.lower() == 'on':
      g.cooler.on()
    elif on_off.lower() == 'off':
      g.cooler.off()
  return 'on' if g.cooler.is_on else 'off'


@control.route('/heater/<on_off>', methods=['GET', 'POST'])
def heater_set(on_off):
  if request.method=='POST':
    if on_off.lower() == 'on':
      g.heater.on()
    elif on_off.lower() == 'off':
      g.heater.off()
  return 'on' if g.heater.is_on else 'off'

@control.route('/temperature/', methods=['GET'])
def temperature():
  return g.thermometer.fahrenheit

@control.route('/mode', methods=['GET'])
@control.route('/mode/<mode>', methods=['POST'])
def mode(mode):
  if request.method=='POST':
    mode = mode.lower()
    if mode in ['off', 'heater', 'cooler', 'auto']:
      session['mode'] = mode
  return session['mode']
