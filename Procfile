release: ./release-tasks.sh
web: python ./manage.py collectstatic --noinput; gunicorn phishtray.wsgi --log-file -
