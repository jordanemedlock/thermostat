import os
from fabric.api import *

requirements_file = 'requirements.txt'


def dev():
  global config_file
  print('Configured for dev')
  env.hosts = ["toddd.local"]
  env.user = "pi"
  config_file = 'dev.cfg'

def prod():
  global config_file
  print('Configured for prod')
  env.hosts = ["babyyoda.local"]
  env.user = "pi"
  config_file = 'prod.cfg'

def pack():
  # build the package
  local('python setup.py sdist --formats=gztar', capture=False)

def setup():
  sudo('apt-get install apache2 python3-pip libapache2-mod-wsgi-py3 git -y')

  sudo('apachectl start')

  sudo('mkdir -p /var/www/thermostat')

  put('apache/001-thermostat.conf', '/tmp/001-thermostat.conf')

  sudo('mv /tmp/001-thermostat.conf /etc/apache2/sites-available/001-thermostat.conf')

  sudo('ln -s /etc/apache2/sites-available/001-thermostat.conf /etc/apache2/sites-enabled/001-thermostat.conf', quiet=True)
  sudo('rm /etc/apache2/sites-available/000-default.conf')

  sudo('apachectl restart')

def install_reqs():
  put(requirements_file, '/tmp/reqs.txt')

  run('pip3 install -r /tmp/reqs.txt')

  run('rm /tmp/reqs.txt')

def install_config():
  put(config_file, '/tmp/configuration.cfg')

  sudo('mv /tmp/configuration.cfg /var/www/thermostat/configuration.cfg')

  run('export APP_SETTINGS=/var/www/thermostat/configuration.cfg')


def deploy():
  # figure out the package name and version
  local('python setup.py sdist --formats=gztar')
  dist = local('python setup.py --fullname', capture=True).strip()
  filename = '%s.tar.gz' % dist

  # upload the package to the temporary folder on the server
  put('dist/%s' % filename, '/tmp/%s' % filename)

  # install the package in the application's virtualenv with pip
  run('pip3 install /tmp/%s' % filename)

  run('rm /tmp/%s' % filename)

  put('apache/thermostat.wsgi', '/tmp/thermostat.wsgi')

  sudo('mv /tmp/thermostat.wsgi /var/www/thermostat/thermostat.wsgi')

  sudo('apachectl restart')
