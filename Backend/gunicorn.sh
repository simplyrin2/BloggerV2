#! /bin/sh

. .venv/bin/activate
export ENV=development
gunicorn __init_app__:app --preload --worker-class gevent --bind 127.0.0.1:8000 --workers=4
deactivate