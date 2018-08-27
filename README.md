# phishtray

[![Build Status](https://travis-ci.com/cybsafe/phishtray.svg?branch=master)](https://travis-ci.com/cybsafe/phishtray)

# Install

Prereq - docker & docker compose. https://docs.docker.com/install/

```

$ docker-compose up -d --build

$ docker exec -it phishtray_web_1 bash
root@1ccee26bd896:/usr/src/app# python manage.py migrate
root@1ccee26bd896:/usr/src/app# python manage.py runserver 0.0.0.0:8000


```
