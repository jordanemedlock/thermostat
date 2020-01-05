from flask import Flask, render_template
import RPi.GPIO as GPIO
import board 
import adafruit_dht

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

heater = 2
ac = 3
something_else = 4
another_thing = 17
heater_on = False
ac_on = False

thermometer = adafruit_dht.DHT11(board.D14)

channels = [heater, ac, something_else, another_thing]

GPIO.setup(channels, GPIO.OUT)
GPIO.output(channels, GPIO.HIGH)


@app.route('/heat/on')
def heat_on():
  heater_on = True
  GPIO.output(heater, GPIO.LOW)
  return "Turning up the heat!"
  
@app.route('/heat/off')
def heat_off():
  heater_on = False
  GPIO.output(heater, GPIO.HIGH)
  return "Turning off the heat!"
  
@app.route('/ac/on')
def ac_on():
  ac_on = True
  GPIO.output(ac, GPIO.LOW)
  return "Turning up the cool!"
  
@app.route('/ac/off')
def ac_off():
  ac_on = False
  GPIO.output(ac, GPIO.HIGH)
  return "Turning off the cool!"

@app.route('/')
def index():
  page = {
    'temp': thermometer.temperature,
	'hum': thermometer.humidity,
	'heater_on': heater_on,
	'ac_on': ac_on
  }
  return render_template('index.html', page=page)
  

if __name__ == '__main__':
  app.run(host='0.0.0.0')
