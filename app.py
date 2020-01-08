from flask import Flask, render_template, g, request
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
  with open('thermostat.json', 'r') as fp:
    return json.load(fp)

def save_thermostat(obj):
  with open('thermostat.json', 'w') as fp:
    json.dump(obj, fp)

@app.route('/', methods=['POST', 'GET'])
def index():
  thermostat = load_thermostat()
  if request.method == 'POST':
    print(request.form)
    thermostat['mode'] = request.form.get('mode') or thermostat['mode']
    thermostat['temp_range'][0] = int(request.form.get('lowest'))
    thermostat['temp_range'][1] = int(request.form.get('lower'))
    thermostat['temp_range'][2] = int(request.form.get('upper'))
    thermostat['temp_range'][3] = int(request.form.get('uppest'))
    save_thermostat(thermostat)
  return render_template('index.html', thermostat=thermostat)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
