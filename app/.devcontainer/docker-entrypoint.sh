#!/bin/bash
# $0 is a script name, $1, $2, $3 etc are passed arguments
# $1 is our command
# Credits: https://rock-it.pl/how-to-write-excellent-dockerfiles/
CMD=$1

# Configure git for the container
configure_git() {
  echo "Configuring git..."
  
  # Ensure vscode user owns the workspace
  sudo chown -R vscode:vscode /workspace 2>/dev/null || true
  
  # Set git to treat the workspace as safe
  git config --global --add safe.directory /workspace
  git config --global --add safe.directory '*'
  
  # Set basic git configuration if not already set
  if [ -z "$(git config --global user.name 2>/dev/null)" ]; then
    git config --global user.name "Dev User"
  fi
  
  if [ -z "$(git config --global user.email 2>/dev/null)" ]; then
    git config --global user.email "dev@example.com"
  fi
  
  # Fix ownership and permissions of git directories
  if [ -d "/workspace/.git" ]; then
    sudo chown -R vscode:vscode /workspace/.git 2>/dev/null || true
    chmod -R u+w /workspace/.git 2>/dev/null || true
  fi
  
  # Set git file mode to false to avoid permission issues
  git config --global core.filemode false
  
  echo "Git configuration complete"
}

wait_for_db () {
  if [ "$DATABASE" = "postgres" ]
  then
      echo "Waiting for postgres..."

      while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
      done

      echo "PostgreSQL started"
  fi
}


setup_django () {
  cd /workspace/app/src

  echo Running migrations
  python manage.py migrate --noinput

  echo Create dummy user if none exists
  python manage.py create_superuser_if_none_exists --user=admin --password=admin

  echo Replace possible default site root page
  python manage.py wagtail_replace_default_site_root_page

  echo Collecting static-files
  python manage.py collectstatic --noinput

  echo Create cache table
  python manage.py createcachetable
}

load_fixture_data() {
  cd /workspace/app/src

  echo Install fixtures

  # python manage.py loaddata pmiek-stripes/fixtures/fixture.json

  echo Fixtures loaded
}

setup_frontend () {
  cd /workspace/app/frontend

  echo Install the Node dependencies
  npm install
}

wait_for_db
configure_git
setup_django
load_fixture_data
setup_frontend

exec "$@"
