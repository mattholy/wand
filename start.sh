#!/bin/bash

required_vars=(
    "WD_SERVER_URL"
    "WD_REDIS_SERVER"
    "WD_POSTGRES_USER"
    "WD_POSTGRES_PWD"
    "WD_POSTGRES_SERVER"
    "WD_POSTGRES_DBNAME"
)
check_env_var() {
    if [ -z "${!1}" ]; then
        echo "Error: Environment variable $1 is not set."
        exit 1
    fi
}
for var in "${required_vars[@]}"; do
    check_env_var "$var"
done

if [ -z "$WD_WORKERS" ]; then
    WD_WORKERS=$((2 * `nproc` + 1))
fi

echo "Number of workers set to: $WD_WORKERS"

gunicorn -w $WD_WORKERS -k uvicorn.workers.UvicornWorker app.main:app --forwarded-allow-ips="*" --bind 0.0.0.0:80
