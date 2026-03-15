#!/bin/bash

set -e

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# activate the virtual environment
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run the application with gunicorn on port 5000
exec gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app
