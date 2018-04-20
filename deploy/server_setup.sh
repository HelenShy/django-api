#!/usr/bin/env bash

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/HelenShy/django-api.git'

PROJECT_BASE_PATH='/usr/local/apps'
VIRTUALENV_BASE_PATH='/usr/local/virtualenvs'

# Set Ubuntu Language
locale-gen en_GB.UTF-8

# Install Python, SQLite and pip
apt-get update
apt-get install -y python3-dev sqlite python-pip supervisor nginx git

# Upgrade pip to the latest version.
pip install --upgrade pip
pip install virtualenv

mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH/django-api

mkdir -p $VIRTUALENV_BASE_PATH
virtualenv --python=python3 $VIRTUALENV_BASE_PATH/django-api

source $VIRTUALENV_BASE_PATH/django_api/bin/activate
pip install -r $PROJECT_BASE_PATH/django-api/requirements.txt

# Run migrations
cd $PROJECT_BASE_PATH/django-api/src

# Setup Supervisor to run our uwsgi process.
cp $PROJECT_BASE_PATH/django-api/deploy/supervisor_django_api.conf /etc/supervisor/conf.d/django_api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart django_api

# Setup nginx to make our application accessible.
cp $PROJECT_BASE_PATH/django-api/deploy/nginx_django_api.conf /etc/nginx/sites-available/django_api.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/django_api.conf /etc/nginx/sites-enabled/django_api.conf
systemctl restart nginx.service

echo "DONE! :)"
