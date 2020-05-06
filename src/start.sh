#!/bin/bash
export FLASK_RUN_PORT=6006
export FLASK_APP=app.py
export app_debug_logs=False
python3 -m flask run --with-threads &
