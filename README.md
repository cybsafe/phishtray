# running the demo

1. Navigate to http://phishtray.local:9000/admin and create an Exercise with emails
1. Copy the exercise UUID
1. In your local terminal, from the phishtray folder, `cd frontend` and `yarn start`
1. Navigate to http://phishtray.local:3000/welcome/<exercise:uuid>/ to start the exercise


# phishtray installation

[![Build Status](https://travis-ci.com/cybsafe/phishtray.svg?branch=master)](https://travis-ci.com/cybsafe/phishtray)

## Prerequisites

1. Install `docker` & `docker compose` - https://docs.docker.com/install/
2. Add the following to your `hosts` file:

        # Phishtray
        127.0.0.1               phishtray.local


## Install

1. Build and bring up the images running `docker-compose up -d --build`
2. Bash in to the django container using `docker-compose exec django bash`  
then create a superuser `py3 manage.py createsuperuser --email your@email.here`

## Running Django Server
1. **Normal** - To run the server normally `make django-run`
2. **Debug** - To run the server in debug mode `make django-debug` (This will allow a tool like PyCharm to actually start the web server within the container)


## Working Within The Container
Within the container you should use Python 3 which can be called via `py3` or `python3.6` commands, `python` refers to Python 2.7 which is the system default. 
