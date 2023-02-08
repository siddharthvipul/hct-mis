#!/bin/bash -x
if [[ ! -z "${PUBLIC_DOMAIN_NAME}" ]]; then
    if [[ ${NGINX_PUBLIC_PORT} != "" && ${NGINX_PUBLIC_PORT} != "80" ]]; then
        PUBLIC_PORT=":${NGINX_PUBLIC_PORT}"
    else
        PUBLIC_PORT=""
    fi
    # SERVER CONFIGURATION
    # export KOBOFORM_URL="${PUBLIC_REQUEST_SCHEME}://${KOBOFORM_PUBLIC_SUBDOMAIN}.${PUBLIC_DOMAIN_NAME}${PUBLIC_PORT}"
    # export KOBOFORM_INTERNAL_URL="http://${KOBOFORM_PUBLIC_SUBDOMAIN}.${INTERNAL_DOMAIN_NAME}" # Always use HTTP internally.
    # export KOBOCAT_URL="${PUBLIC_REQUEST_SCHEME}://${KOBOCAT_PUBLIC_SUBDOMAIN}.${PUBLIC_DOMAIN_NAME}${PUBLIC_PORT}"
    # export ENKETO_URL="${PUBLIC_REQUEST_SCHEME}://${ENKETO_EXPRESS_PUBLIC_SUBDOMAIN}.${PUBLIC_DOMAIN_NAME}${PUBLIC_PORT}"
    export SESSION_COOKIE_DOMAIN=".${PUBLIC_DOMAIN_NAME}"
    export DJANGO_ALLOWED_HOSTS=".${PUBLIC_DOMAIN_NAME} .${INTERNAL_DOMAIN_NAME} kubernetes.internal"
    
    export KPI_DATABASE_URL="postgis://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${KPI_POSTGRES_DB}"
    export KC_DATABASE_URL="postgis://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${KOBOCAT_POSTGRES_DB}"
    export KOBOCAT_BROKER_URL="redis://:${REDIS_PASSWORD}@redis-main-master:6379/2"
    export CACHE_URL="redis://:${REDIS_PASSWORD}@redis-main-master:6379/2"
    export SERVICE_ACCOUNT_BACKEND_URL="redis://:${REDIS_PASSWORD}@redis-main-master:6379/6"

    
    # DATABASE
    export DATABASE_URL="${KC_DATABASE_URL}"
    export POSTGRES_DB="${KOBOCAT_POSTGRES_DB}"
    
    # OTHER
    # export KOBOCAT_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
    # export KOBOCAT_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}"
    export KPI_URL="${KOBOFORM_URL}"
    export KPI_INTERNAL_URL="${KOBOFORM_INTERNAL_URL}"  # Copy the same logic as before but why do we need another variable?
    export RAVEN_DSN="${KOBOCAT_RAVEN_DSN}"
else
    echo 'Please fill out your `envfile`!'
    exit 1
fi
