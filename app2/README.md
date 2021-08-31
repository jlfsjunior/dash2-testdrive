# Long Callback tests

## Using diskcache

Not much to be said... It works ok in a single server setup or for testing, but not interesting for production.

## Using Celery/Redis

Here things get more interesting. Firstly, before I forget it, these are the two steps to run the example in `app2/celery_app.py`:

1. Start a Docker container using the redis image:

```sh
docker run -d -p 6379:6379 redis
```

2. Run celery worker server:

```sh
celery -A celery_app.celery worker --loglevel=INFO
```

Then the app is ready to run (in a dev environment):

```sh
python celery_app.py
```