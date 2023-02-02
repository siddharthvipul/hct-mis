#!/bin/bash

set -e

case "$1" in
    "test")
        echo "Waiting for backend to be ready"
        waitforit -host=backend -port=8000 --timeout 600
        echo "Waiting for frontend to be ready"
        waitforit -host=frontend -port=3000 --timeout 600
        yarn cypress run --headless --config baseUrl=http://proxy
        ;;
    *)
        exec "$@"
        ;;
esac