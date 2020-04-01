release: ./release-tasks.sh
web: python ./manage.py collectstatic --noinput; gunicorn --timeout=10 --worker-class=gevent --worker-connections=1000 --workers=3 phishtray.wsgi:application --log-file -
