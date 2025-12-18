#!/bin/bash
set -e

echo "========================================"
echo "Starting hail application with cache warming"
echo "========================================"

# Start the uvicorn server in the background
echo "Starting uvicorn server..."
poetry run uvicorn app:app --host 0.0.0.0 --port 7000 &
UVICORN_PID=$!

# Function to handle shutdown signals
cleanup() {
    echo "Shutting down..."
    
    # Terminate cache warming process if it's still running
    if [ ! -z "$WARM_CACHE_PID" ]; then
        kill $WARM_CACHE_PID 2>/dev/null || true
    fi
    
    # Terminate uvicorn server
    kill $UVICORN_PID 2>/dev/null || true
    
    exit 0
}

trap cleanup SIGTERM SIGINT

# Wait a moment for the server to initialize
sleep 3

# Wait for Redis to be ready
echo "Waiting for Redis to be ready..."
REDIS_HOST="${REDIS_HOST:-localhost}"
REDIS_PORT="${REDIS_PORT:-6379}"
MAX_RETRIES=30
RETRY_COUNT=0

until poetry run python - <<EOF 2>/dev/null
import os
import redis
redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=int(os.environ.get('REDIS_PORT', 6379)),
    socket_connect_timeout=1
).ping()
EOF
do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "⚠ Redis did not become ready within timeout period"
        echo "  Proceeding anyway, but application may experience errors"
        break
    fi
    echo "  Waiting for Redis... (attempt $RETRY_COUNT/$MAX_RETRIES)"
    sleep 1
done

if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
    echo "✓ Redis is ready"
    
    # Run the cache warming script in the background
    echo "Starting cache warming process..."
    poetry run python scripts/warm_cache.py &
    WARM_CACHE_PID=$!

    # Wait for the cache warming to complete (optional - it runs independently)
    wait $WARM_CACHE_PID
    WARM_EXIT_CODE=$?

    if [ $WARM_EXIT_CODE -eq 0 ]; then
        echo "✓ Cache warming completed successfully"
    else
        echo "⚠ Cache warming encountered issues (exit code: $WARM_EXIT_CODE)"
        echo "  Application will continue running with cold cache"
    fi
else
    echo "⚠ Skipping cache warming - Redis is not available"
fi

# Keep the uvicorn server running
echo "Application is running. Monitoring uvicorn process (PID: $UVICORN_PID)..."
wait $UVICORN_PID
