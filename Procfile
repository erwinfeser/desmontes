web: gunicorn econativo.wsgi
worker: celery worker -A econativo --beat -c 2 --without-gossip --without-mingle --heartbeat-interval=10 --loglevel=info