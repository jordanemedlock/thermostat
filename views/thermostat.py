from flask import Blueprint, g
from werkzeug.routing import BaseConverter

thermostat = Blueprint('thermostat', __name__)

class ModeConverter(BaseConverter):
	modes = {
		g.thermostat.HEATER: g.thermostat.HEATER,
		g.thermostat.COOLER: g.thermostat.COOLER,
		g.thermostat.AUTO: g.thermostat.AUTO,
		g.thermostat.OFF: g.thermostat.OFF,
	}
	def to_python(self, value):
		value = value.lower()
		if value not in self.modes:
			raise ValidationError()
		return value

	def to_url(self, value):
		value = value.lower()
		if value not in self.modes:
			raise ValidationError()
		return value

thermostat.url_map.converters['mode'] = ModeConverter

@thermostat.route('/set-mode/<mode:mode>')
def 
# TODO: continue here