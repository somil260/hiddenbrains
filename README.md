Simple registration App

1. Install virtual environment using
	virtualenv -p python3 <environment name>
	$ virtualenv -p python3 env

2. Enable virtualenv 
 	$ source env/bin/activate

3. goto inside project folder  location and start the server
	$ python manage.py runserver


in new tab Running RabbitMQ

$ sudo rabbitmq-server

Running Celery

$ celery -A my_app worker -l info