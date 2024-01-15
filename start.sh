#!/bin/bash

if [ -z "$WD_WORKERS" ]; then
    WD_WORKERS=$((2 * `nproc` + 1))
fi

gunicorn -w $WD_WORKERS -k uvicorn.workers.UvicornWorker app.main:app --forwarded-allow-ips="*" --bind 0.0.0.0:80
