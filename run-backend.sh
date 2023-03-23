#!/bin/bash

cd backend

celery -A task worker &

python app.py $1
