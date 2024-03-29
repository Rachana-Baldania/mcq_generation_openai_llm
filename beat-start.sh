#! /usr/bin/env bash
set -e

celery -A app.worker beat -l info