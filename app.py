from flask import Flask, render_template, g, request
import os
import json
import views
import apscheduler.schedulers.background as aps

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


# @app.before_first_request
# def activate_thermostat():
#   def run_job():
#     while True:
#       print("Running thermostat")
#       time.sleep(30)

#   thread = threading.Thread(target=run_job)
#   thread.start()

scheduler = aps.BackgroundScheduler()
scheduler.start()

app.register_blueprint(views.control)
app.register_blueprint(views.ui)

app.secret_key = b'suck my dick'


views.activate_thermostat(scheduler)
print(app.url_map)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
