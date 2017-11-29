#!/bin/sh

pip install -U -r requirements.txt

exec gunicorn --config=/app/gunicorn.py uf_values_api.wsgi
