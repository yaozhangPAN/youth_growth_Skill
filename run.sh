#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
exec gunicorn -b "0.0.0.0:${HTTP_PORT:-5005}" 'apps:create_app()' --factory
