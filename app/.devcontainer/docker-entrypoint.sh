#!/bin/bash
# $0 is a script name, $1, $2, $3 etc are passed arguments
# $1 is our command
# Credits: https://rock-it.pl/how-to-write-excellent-dockerfiles/
CMD=$1

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
  cd /workspace/src

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
  cd /workspace/src

  echo Install fixtures

  # python manage.py loaddata pmiek-stripes/fixtures/fixture.json

  echo Fixtures loaded
}

setup_frontend () {
  cd /workspace/frontend

  echo Install the Node dependencies
  npm install
}

wait_for_db
setup_django
load_fixture_data
setup_frontend

exec "$@"
