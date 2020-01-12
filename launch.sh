su - pi
cd /home/pi/thermostat
/home/pi/.local/bin/waitress-serve --port=5000 --url-scheme=http thermostat:app
