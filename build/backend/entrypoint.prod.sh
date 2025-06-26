#!/usr/bin/env bash


exec uvicorn main:app --host 0.0.0.0 --reload --port 8000 -workers 2
