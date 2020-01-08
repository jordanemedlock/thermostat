from flask import Flask, render_template, g, request
from models import Heater, AC, Thermometer, TempRange, Thermostat
import os
import json

app = Flask(__name__)

@app.template_filter('bool_change')
def bool_change_filter(value, true_value, false_value):
  if value:
    return true_value
  else:
    return false_value

@app.template_filter('on_off')
def on_off_filter(value):
  return bool_change_filter(value, 'On', 'Off')

@app.template_filter('active')
def active_filter(value, target):
  return bool_change_filter(value==target, 'active', '')

@app.template_filter('checked')
def checked_filter(value, target):
  return bool_change_filter(value==target, 'checked', '')

def load_thermostat():
  try: 
    with open('thermostat.json', 'r') as fp:
      obj = json.load(fp)

    return Thermostat.from_json(obj)
  except:
    heater = Heater(2)
    ac = AC(3)
    thermometer = Thermometer(14)
    temp_range = TempRange(65, 67, 78, 80)
    return Thermostat(heater, ac, thermometer, temp_range, Thermostat.AUTO)

def save_thermostat(thermostat):
  obj = thermostat.to_json()
  with open('thermostat.json', 'w') as fp:
    json.dump(obj, fp)

@app.route('/', methods=['POST', 'GET'])
def index():
  thermostat = load_thermostat()
  if request.method == 'POST':
    print(request.form)
    mode = request.form.get('mode')
    thermostat.temp_range.lowest = int(request.form.get('lowest'))
    thermostat.temp_range.lower = int(request.form.get('lower'))
    thermostat.temp_range.upper = int(request.form.get('upper'))
    thermostat.temp_range.uppest = int(request.form.get('uppest'))
    if mode:
      thermostat.set_mode(mode)
    save_thermostat(thermostat)
  return render_template('index.html', thermostat=thermostat)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
