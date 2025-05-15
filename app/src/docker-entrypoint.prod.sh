#!/bin/bash
# $0 is a script name, $1, $2, $3 etc are passed arguments
# $1 is our command
# Credits: https://rock-it.pl/how-to-write-excellent-dockerfiles/
CMD=$1

wait_for_db () {
    # Wait until postgres is ready
    until nc -z $DB_HOST 5432; do
        echo "$(date) - waiting for postgres... ($DB_HOST:5432)"
        sleep 3
    done
}

setup_django () {
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

wait_for_db
setup_django

if [ -z "$N_WORKERS" ]
then
    N_CORES=$(grep -c ^processor /proc/cpuinfo)
    # recommended by http://docs.gunicorn.org/en/stable/design.html#how-many-workers
    N_WORKERS=$(( N_CORES * 2 + 1 ))
fi

echo Starting using gunicorn
exec gunicorn pipit.wsgi:application --bind 0.0.0.0:8000 --workers ${N_WORKERS} --timeout 60 --graceful-timeout 60
