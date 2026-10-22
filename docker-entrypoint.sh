#!/bin/sh
set -e

# Wait for MySQL (skipped when running on sqlite, e.g. DAST container)
if [ "${DB_ENGINE:-mysql}" != "sqlite" ]; then
  echo "Waiting for database at ${DB_HOST:-localhost}:${DB_PORT:-3306} ..."
  python - <<PY
import os, socket, sys, time
host, port = os.environ.get("DB_HOST", "localhost"), int(os.environ.get("DB_PORT", "3306"))
for _ in range(60):
    try:
        socket.create_connection((host, port), 2).close()
        sys.exit(0)
    except OSError:
        time.sleep(2)
print("Database not reachable"); sys.exit(1)
PY
fi

if [ "${RUN_MIGRATIONS:-0}" = "1" ]; then
  python manage.py migrate --noinput
fi

exec "$@"