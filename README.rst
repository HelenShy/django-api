DJANGO-API
==========
REST API application that allows to search for lyrics and video by artist name and lyrics title and save them in personal collection.

Local installation:
-------------------------------------------------------------

1. Create and configurate machine according to Vagrantfile.

.. code-block:: bash

    $ vagrant up
   
2. SSH into a running Vagrant machine and gets you an access to a shell.

.. code-block:: bash

    $ vagrant ssh
    
3. Create virtualenv.

.. code-block:: bash

    $ mkvirtualenv django-api --python=python3
    
4. Install django and django-rest insedi virtualenv.

.. code-block:: bash

    (profiles-api)$ pip install django==1.11
    (profiles-api)$ pip install djangorestframework==3.6.2

5. Create super user in django app and run app.

.. code-block:: bash

    (profiles-api)$ cd /vagrant/src/django_project
    (profiles-api)$ python manage.py createsuperuser
    (profiles-api)$ python manage.py runserver 0.0.0.0:8080


Installation on AWS EC2 machine:
-------------------
1. Connect to AWS server on EC2 machine.

.. code-block:: bash

    $ ssh -i "[your_path].pem" ubuntu@[...].compute.amazonaws.com
    
In ``settings.py`` set ALLOWED_HOSTS to AWS EC2 path
   
2. Load setup file on AWS server.

.. code-block:: bash

    $ wget https://raw.githubusercontent.com/HelenShy/django-api/master/deploy/server_setup.sh

3. Make setup file executable and execute it.

.. code-block:: bash

    $ chmod +x server_setup.sh
    $ sudo ./server_setup.sh
    
4. Change to the root server user and activate virtualenv.

.. code-block:: bash

    $ sudo -i
    $ source /usr/local/virtualenvs/django_api/bin/activate
    
5. Setup django app: migrate database, create auper user.

.. code-block:: bash

    (profiles-api)$ cd /usr/local/apps/django-api/src/django_project/
    (profiles-api)$ python manage.py migrate
    (profiles-api)$ python manage.py createsuperuser
    (profiles-api)$ supervisorctl restart all
