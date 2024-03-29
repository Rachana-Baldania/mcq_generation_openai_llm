#! /usr/bin/env bash
set -e

celery -A app.worker worker -l info -c 1