# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT=3.11-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}
LABEL version="v0.1.0"

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=pipit.settings.local \
    ALLOWED_HOSTS=* \
    INTERNAL_IPS=0.0.0.0 \
    SECRET_KEY=generatesecretkeyhere \
    MEDIA_PATH=/workspace/media \
    STATIC_PATH=/workspace/static \
    REQUIREMENTS=local.txt \
    DB_USER=postgres \
    DB_PASSWORD=postgres \
    DB_NAME=stripes \
    DB_HOST=db \
    PYTHONPATH="${PYTHONPATH}:/workspace"

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
COPY ./src/requirements/local.txt /tmp/pip-tmp/
COPY ./src/requirements/test.txt /tmp/pip-tmp/
COPY ./src/requirements/base.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/local.txt \
    && rm -rf /tmp/pip-tmp

RUN pip install --upgrade pip \
    && pip install ipython ipdb

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    && apt-get install -y netcat gcc libpq-dev \
    && apt-get install -y binutils libproj-dev gdal-bin \
    && apt-get install -y vim curl gettext \
    && apt-get install -y libmagickwand-dev \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000
