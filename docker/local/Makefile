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

.PHONY: django-shell
django-shell:
	docker-compose exec django bash -c "pip install ipython &&  python3.6 ./manage.py shell_plus"

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

.PHONY: django-fake-users-0001
django-fake-users-0001:
	docker-compose exec django bash -c "echo \"INSERT INTO django_migrations (app, name, applied) VALUES ('users', '0001_initial', CURRENT_TIMESTAMP);\" | python3.6 manage.py dbshell"
	docker-compose exec django bash -c "echo \"UPDATE django_content_type SET app_label = 'users' WHERE app_label = 'auth' and model = 'user';\" | python3.6 manage.py dbshell"

.PHONY: django-fake-users-0002
django-fake-users-0002:
	docker-compose exec django bash -c "echo \"INSERT INTO django_migrations (app, name, applied) VALUES ('users', '0002_auto_20190930_1718', CURRENT_TIMESTAMP);\" | python3.6 manage.py dbshell"
# ==================================================
