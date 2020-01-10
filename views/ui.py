from flask import Blueprint, g, render_template

ui = Blueprint('ui', __name__)

@ui.route('/')
def index():
  page = {
    'temp': 65,
    'mode': 'auto',
    'heater': 'On',
    'cooler': 'Off',
    'temp_range': [65,67,78,80]
  }
  return render_template('index.html', page=page)