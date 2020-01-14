import os


os.environ['APP_SETTINGS'] = 'debug.cfg'


from thermostat import create_app
application = create_app()