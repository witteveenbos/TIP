# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the required files into the container
COPY . .

# Install dependencies
RUN pip install poetry && poetry install --no-interaction --no-ansi --without dev --no-root

# Make the entrypoint script executable
RUN chmod +x scripts/docker-entrypoint-with-cache-warming.sh

# Set environment variables
ENV REDIS_HOST=${REDIS_HOST}
ENV REDIS_PORT=${REDIS_PORT}
ENV REDIS_PASSWORD=${REDIS_PASSWORD}
ENV ETM_API_KEY=${ETM_API_KEY}
ENV TRUSTED_ORIGINS_DATA=${TRUSTED_ORIGINS_DATA}
ENV SUPER_SECRET_KEY=${SUPER_SECRET_KEY}

# Default base URL for cache warming
ENV HAIL_BASE_URL=http://localhost:7000

CMD ["./scripts/docker-entrypoint-with-cache-warming.sh"]