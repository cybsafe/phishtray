
[![Build Status](https://travis-ci.com/cybsafe/phishtray.svg?branch=master)](https://travis-ci.com/cybsafe/phishtray)
[![Coverage Status](https://coveralls.io/repos/github/cybsafe/phishtray/badge.svg?branch=master)](https://coveralls.io/github/cybsafe/phishtray?branch=master)

# Running The Demo

0. make sure you've completed the prereqs
1. Navigate to http://phishtray.local:9000/admin and create an Exercise with emails
1. Copy the exercise UUID
1. In your local terminal, from the phishtray folder, `cd frontend` and `yarn start`
1. Navigate to http://phishtray.local:3000/welcome/<exercise:uuid>/ to start the exercise


# Phishtray Installation


## Prerequisites

1. Install `docker` & `docker compose` - https://docs.docker.com/install/
2. Add the following to your `hosts` file:

        # Phishtray
        127.0.0.1               phishtray.local
3. Create two env files in the frontend. One called `.env.development.local` and the other called `.env.local`. You should then ask one of the devs for the content of the files.

## Install
1. Go into the local docker directory `cd docker/local`
2. Build and bring up the images running `docker-compose up -d --build`
3. Bash in to the django container using `docker-compose exec django bash`  
then create a superuser `py3 manage.py createsuperuser --email your@email.here`
4. Run the static files command `py3 manage.py collectstatic`

## Running tests
Run bash inside the django container using `docker-compose exec django bash`
then run the following test command `py3 manage.py test`

## Running Django Server
1. **Normal** - To run the server normally `make django-run`
2. **Debug** - To run the server in debug mode `make django-debug` (This will allow a tool like PyCharm to actually start the web server within the container)


## Working Within The Container
Within the container you should use Python 3 which can be called via `py3` or `python3.6` commands, `python` refers to Python 2.7 which is the system default. 
