from flask import Flask, render_template, g
from .models import Heater, AC, Thermometer, TempRange, Thermostat

app = Flask(__name__)

heater = Heater(2)
ac = AC(3)
thermometer = Thermometer(14)
temp_range = TempRange(65, 67, 78, 80)

g.thermostat = Thermostat(heater, ac, thermometer, temp_range, Thermostat.AUTO)


@app.route('/')
def index():
  global set_temp, heater_mode, ac_is_on
  page = {
    'temp': to_f(thermometer.temperature),
    'set_temp': to_f(set_temp),
    'hum': thermometer.humidity,
    'heater_on': heater_mode,
    'ac_on': ac_is_on
  }
  return render_template('index.html', page=page)
  

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
