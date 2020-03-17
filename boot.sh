#!/bin/sh
source venv/bin/activate
exec gunicorn -b :5100 --access-logfile - --error-logfile - bulletin:app