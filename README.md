# Gallery WebSockets base

This repository contains the base implementation of our spring quarter gallery, which uses websockets via Django Channels and react-use-websocket to share folks' positions in the world created in React-three-fiber.

In a future update, it will also save these positions and show others' paths through the gallery.

#### Key commands for development
(using docker for Redis locally)

*to run the app*
`daphne djsr.asgi:application `
`celery worker --app djsr.celery.app --loglevel info`
`docker start django-websockets`
`docker run --name django-websockets -d -p 6379:6379 redis`  OR `docker start django-websockets`

docker run --name django-websockets -d -p 6379:6379 redis
docker start django-websockets
docker exec -it fc90772e7b8893f18600c56c746b862ce2c05f7d6bbe895b95879a4a4e94a368 redis-cli
monitor
docker system prune