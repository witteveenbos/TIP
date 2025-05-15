# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the required files into the container
COPY . .

# Install dependencies
RUN pip install poetry && poetry install --no-interaction --no-ansi --without dev --no-root

# Set environment variables
ENV REDIS_HOST=${REDIS_HOST}
ENV REDIS_PORT=${REDIS_PORT}