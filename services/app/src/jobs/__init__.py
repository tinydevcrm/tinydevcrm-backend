"""
Jobs service.

This Django app manages API endpoints related to managing 'pg_cron'-based
scheduling around data lifecycles, particularly around refreshing materialized
views.

This scheduling service is colocated with the database in order to keep the
scheduling logic defined within the same runtime as the data management service,
which may help reduce fault model considerations. It also translates 'cron',
originally a file based with /etc/crontab, into a PostgreSQL table persisted as
/var/lib/postgresql/data, which may benefit from PostgreSQL's
replication/backup/clustering strategies.
"""
