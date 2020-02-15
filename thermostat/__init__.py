from flask import Flask, render_template, g, request
import os
import json
from thermostat import views
import apscheduler.schedulers.background as aps
import logging

logging.basicConfig(
  filename='thermostat.log', 
  level=logging.DEBUG,
  format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  app.debug = True
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
    with app.app_context():
      views.activate_thermostat(app, scheduler, app.config)

  return app