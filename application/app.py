import time
import os

import redis
from flask import Flask

app = Flask(__name__)

redis_host = os.environ['DATABASE_URL']
redis_password = os.environ['DATABASE_PASSWORD']
redis_port = int(os.environ['DATABASE_PORT'])

cache = redis.Redis(host=redis_host, password=redis_password, port=redis_port)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
