import os


os.environ['APP_SETTINGS'] = '/var/www/thermostat/configuration.cfg'


from thermostat import create_app
application = create_app()