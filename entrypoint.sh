#!/bin/bash

DEFAULT_UVICORN_LOG_LEVEL=info
export UVICORN_LOG_LEVEL=${UVICORN_LOG_LEVEL:-$DEFAULT_UVICORN_LOG_LEVEL}

DEFAULT_CELERY_LOG_LEVEL=INFO
export CELERY_LOG_LEVEL=${CELERY_LOG_LEVEL:-$DEFAULT_CELERY_LOG_LEVEL}

log() {
  if [[ $# -eq 1 ]]; then
    local message="$1" level="INFO"
  else
    local message="$1" level="$2"
  fi

  logstring="$(date) -- [$level]: $message"

  if [[ level -eq "WARNING" || level -eq "ERROR" ]]; then
    echo "$logstring" >&2
  else
    echo "$logstring"
  fi
}

run_api() {
  log "Starting App API..."
  alembic upgrade head
  exec uvicorn --reload --host 0.0.0.0 --port 8090 --log-level "$UVICORN_LOG_LEVEL" app.app:app
}

run_worker_with_beat() {
  log "Starting App Celery worker with Celery beat, monitored by watchgod..."
  exec watchgod celery.__main__.main --args -A app.worker.app:celery_app worker -B -l "$CELERY_LOG_LEVEL"
}

run_worker() {
  log "Starting App Celery worker..."
  exec celery -A app.worker.app:celery_app worker -l "$CELERY_LOG_LEVEL"
}

run_scheduler() {
  log "Starting App Celery beat..."
  exec celery -A app.worker.app:celery beat -l "$CELERY_LOG_LEVEL"
}

if [[ $# -eq 0 ]]; then
  run_api
else
  case "$1" in
  api)
    run_api
    ;;
  worker_with_beat)
    run_worker_with_beat
    ;;
  worker)
    run_worker
    ;;
  scheduler)
    run_scheduler
    ;;
  *)
    exec "$@"
    ;;
  esac
fi
