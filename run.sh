#!/bin/bash

set -e

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt
exec gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app
