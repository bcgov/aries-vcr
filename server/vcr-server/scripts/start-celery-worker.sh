#!/bin/bash

# Start the tob-api as a Celery worker node.
echo "Starting an instance of the tob-api as a Celery worker node ..."
celery -A subscriptions worker -E -l INFO
