#!/bin/sh
# Cloud Run sets PORT (usually 8080). Rewrite nginx listen to match, then start.
set -e
PORT="${PORT:-8080}"
CONF=/etc/nginx/conf.d/default.conf

# Replace any listen <port> with the runtime PORT
sed -i "s/listen [0-9][0-9]* /listen ${PORT} /g" "$CONF"

# Show what we will run (appears in Cloud Run logs)
echo "Starting nginx on 0.0.0.0:${PORT}"
nginx -t
exec nginx -g 'daemon off;'
