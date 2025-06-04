# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /workspace

# Copy the requirements file into the container
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN pip install poetry && poetry install --no-root

# Install additional dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    && apt-get install -y git vim curl

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV REDIS_HOST=${REDIS_HOST}
ENV REDIS_PORT=${REDIS_PORT}