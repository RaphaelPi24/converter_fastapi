#!/usr/bin/env bash


exec uvicorn main:app --host 0.0.0.0 --reload
#exec gunicorn -c gunicorn.py app:app