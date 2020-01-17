from flask import Flask, render_template, g, request
import os
import json
import views
import apscheduler.schedulers.background as aps
from sassutils.builder import build_directory

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


@app.before_request
def compile_css():
  os.system('sass static/css')

scheduler = aps.BackgroundScheduler()
scheduler.start()

app.register_blueprint(views.control)
app.register_blueprint(views.ui)

app.secret_key = b'suck my dick'


views.activate_thermostat(scheduler)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
