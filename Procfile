release: python manage.py migrate --noinput
web: daphne djsr.asgi:application --port $PORT --bind 0.0.0.0
worker: REMAP_SIGTERM=SIGQUIT celery worker --app djsr.celery.app --loglevel info