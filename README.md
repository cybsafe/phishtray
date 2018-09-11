# phishtray

[![Build Status](https://travis-ci.com/cybsafe/phishtray.svg?branch=master)](https://travis-ci.com/cybsafe/phishtray)

# Prerequisites

1. Install `docker` & `docker compose` - https://docs.docker.com/install/
2. Add the following to your `hosts` file:

        # Phishtray
        127.0.0.1               phishtray.local


# Install

1. Build and bring up the images running `docker-compose up -d --build`
2. Bash in to the django container using `docker-compose exec django bash`  
then create a superuser `python manage.py createsuperuser --email your@email.here`
3. Run the server normally `make django-run`
4. Run the server in debug mode `make django-debug` (This will need a tool like PyCharm to actually start the web server within the container) 


