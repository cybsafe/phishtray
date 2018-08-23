# phishtray

[![Build Status](https://travis-ci.com/cybsafe/phishtray.svg?branch=master)](https://travis-ci.com/cybsafe/phishtray)

# Install

Prereq - docker & docker compose. https://docs.docker.com/install/

```

$ docker-compose up -d --build

$ docker exec -it phishtray_web_1 bash
then inside the container:
$ python manage.py migrate
$ python manage.py createsuperuser --email your@email.here
$ python manage.py runserver 0.0.0.0:8000
```
