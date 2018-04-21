REST API application that allows to search for lyrics and video by artist name and lyrics title and save them in personal collection.

To expand environment locally proceed through the next steps:

1. Run *vagrant up* - creates and configurates a machine according to Vagrantfile.
2. Run *vagrant ssh* - SSH into a running Vagrant machine and gets you an access to a shell.
3. mkvirtualenv django-api --python=python3 - creates virtualenv
4. pip install django==1.11
5. pip install djangorestframework==3.6.2
6. cd /vagrant/src/django_project
   python manage.py createsuperuser - creates super user an django app
7. python manage.py runserver 0.0.0.0:8000 


Machine up on AWS:

1. ssh -i "[your_path].pem" ubuntu@[...].compute.amazonaws.com
   -connect to AWS server
   in settings.py set ALLOWED_HOSTS to AWS path
2. wget https://raw.githubusercontent.com/HelenShy/django-api/master/deploy/server_setup.sh - load setup file on AWS server
3. chmod +x server_setup.sh - make setup file executable
4. sudo ./server_setup.sh - execute setup file
5. sudo -i - changes to the root server user
6. source /usr/local/virtualenvs/django_api/bin/activate - activate virtualenv
7. cd /usr/local/apps/django-api/src/django_project/
8. python manage.py migrate
9. python manage.py createsuperuser
10. supervisorctl restart all