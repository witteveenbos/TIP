FROM python:3.11-slim as base

# Create app directory
RUN mkdir -p /home/app

# Create directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install server packages
RUN apt-get update \
    && apt-get install -y netcat-traditional gcc libpq-dev \
    && apt-get install -y binutils libproj-dev gdal-bin \
    && apt-get install -y vim curl gettext \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install pip --upgrade
ADD requirements $APP_HOME/requirements
RUN pip install -r ./requirements/prod.txt

# Copy project
COPY . $APP_HOME

FROM base AS wagtail
RUN pip install gunicorn

# Chown all files
RUN chmod -R +x $APP_HOME

RUN chmod +x ./docker-entrypoint.prod.sh

# Run entrypoint.prod.sh
ENTRYPOINT ["sh", "docker-entrypoint.prod.sh", "gunicorn"]
