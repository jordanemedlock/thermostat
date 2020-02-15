from flask import Blueprint, g, render_template, current_app
import os

ui = Blueprint('ui', __name__)

@ui.before_request
def compile_css():
  if current_app.config['ENV'] == 'development':
    os.system('sass thermostat/static/css')
    print('compiled css')

@ui.before_request
def compile_js():
  if current_app.config['ENV'] == 'development':
    os.system('tsc -p thermostat/static/js')
    print('compiled js')

@ui.route('/')
def index():
	return render_template('index.html')