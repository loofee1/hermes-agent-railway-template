#!/bin/sh

set -eu

export HERMES_DASHBOARD_PORT="${HERMES_DASHBOARD_PORT:-${PORT:-8080}}"

exec /opt/hermes/docker/entrypoint-dispatch.sh "$@"
