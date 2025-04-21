#!/usr/bin/env bash

exec uvicorn primit_main:app --host 0.0.0.0 --reload
