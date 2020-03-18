#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

export BASEDIR='/usr/src/app'

python ${BASEDIR}/src/manage.py flush --no-input
python ${BASEDIR}/src/manage.py migrate
python ${BASEDIR}/src/manage.py collectstatic --no-input --clear

exec "$@"
