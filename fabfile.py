import os
from fabric.api import *



def dev():
  global requirements_file, config_file
  print 'Configured for dev'
  env.hosts = ["trover.local"]
  env.user = "pi"
  requirements_file = 'requirements/dev.txt'
  config_file = 'dev.cfg'

def test():
  print 'Configured for test'
  env.hosts = ["10.1.1.2"]
  env.user = "glassfish"
  requirements_file = 'requirements/prod.txt'
  config_file = 'prod.cfg'

def pack():
  # build the package
  local('python setup.py sdist --formats=gztar', capture=False)

def install_reqs():
  put(requirements_file, '/tmp/reqs.txt')

  run('pip3 install -r /tmp/reqs.txt')

  run('rm /tmp/reqs.txt')

def install_config():
  put(config_file, '/var/www/thermostat/configuration.cfg')

  run('export APP_SETTINGS=/var/www/thermostat/configuration.cfg')


def deploy():
  # figure out the package name and version
  dist = local('python setup.py --fullname', capture=True).strip()
  filename = '%s.tar.gz' % dist

  # upload the package to the temporary folder on the server
  put('dist/%s' % filename, '/tmp/%s' % filename)

  # install the package in the application's virtualenv with pip
  run('pip3 install /tmp/%s' % filename)

  # remove the uploaded package
  # run('rm -r /tmp/%s' % filename)

  put('thermostat.wsgi', '/var/www/thermostat/thermostat.wsgi')
