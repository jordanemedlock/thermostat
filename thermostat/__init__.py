from flask import Flask, render_template, g, request
import os
import json
from thermostat import views
import apscheduler.schedulers.background as aps

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_envvar('APP_SETTINGS')

  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  scheduler = aps.BackgroundScheduler()
  scheduler.start()

  app.register_blueprint(views.control)
  app.register_blueprint(views.ui)

  if app.config.get('RUN_THERMOSTAT'):
    views.activate_thermostat(scheduler, app.config)

  return app