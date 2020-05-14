release: python djsr/manage.py migrate --noinput
web: cd djsr && daphne djsr.asgi:application --port $PORT --bind 0.0.0.0
worker: REMAP_SIGTERM=SIGQUIT cd djsr && celery worker --app djsr.celery.app --loglevel info