.PHONY: clean
clean:
	- docker-compose kill
	- docker-compose rm
	- rm -rf db

.PHONY: stop
stop:
	docker-compose stop


# DEV COMMANDS
# ==================================================
.PHONY: django-run
django-run:
	docker-compose exec django bash -c "python3.6 /usr/src/app/manage.py runserver 0:9000"

.PHONY: django-run-detached
django-run-detached:
	docker-compose exec -d django bash -c "python3.6 /usr/src/app/manage.py runserver 0:9000"

.PHONY: django-test
django-test:
	docker-compose exec django bash -c "python3.6 /usr/src/app/manage.py test"
# ==================================================


# SSH COMMANDS (to debug via ssh)
# ==================================================
.PHONY: django-debug
django-debug:
	ssh-keygen -R '[phishtray.local]:9022'
	docker-compose exec -d django bash -c "/usr/bin/ssh-keygen -A; /usr/sbin/sshd -D"

.PHONY: django-ssh
django-ssh:
	ssh -p9022 root@phishtray.local -t 'cd /usr/src/app; bash -l'
# ==================================================


# MIGRATION COMMANDS
# ==================================================
.PHONY: django-makemigrations
django-makemigrations:
	docker-compose exec django bash -c "python3.6 /usr/src/app/manage.py makemigrations"

.PHONY: django-migrate
django-migrate:
	docker-compose exec django bash -c "python3.6 /usr/src/app/manage.py migrate"

.PHONY: django-showmigrations
django-showmigrations:
	docker-compose exec django bash -c "python3.6 /usr/src/app/manage.py showmigrations"
# ==================================================
