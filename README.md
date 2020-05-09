daphne djsr.asgi:application 
celery worker --app djsr.celery.app --loglevel info

docker run --name django-websockets -d -p 6379:6379 redis
socker start django-websockets
docker exec -it fc90772e7b8893f18600c56c746b862ce2c05f7d6bbe895b95879a4a4e94a368 redis-cli
monitor
docker system prune