#!/bin/bash

cd backend

celery -A task worker
