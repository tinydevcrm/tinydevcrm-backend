from django.apps import AppConfig


# NOTE: This is where Django lifecycle methods would go.
#
# TODO: During Django app startup, make sure that the PostgreSQL compute
# instance has authority to run cron jobs. See Stack Overflow answer:
# https://stackoverflow.com/a/44657411/1497211. Currently, with the Docker
# container in PostgreSQL using the root user, this isn't a problem, however,
# running as root in production may cause significant security issues.
#
# TODO: During Django app startup, make sure to configure a cron job in order to
# export the 'jobs_eventrefreshes' table to S3 Glacier or something, truncate
# the table, and add itself back to the cron job. Maybe configure a PL/Python
# stored procedure to do so. Otherwise, the table will continue expanding until
# the table becomes too big, and the database keels over. I could truncate the
# table upon issuing a 'pg_notify()' in the stored procedure...
#
# TODO: See whether the 'jobs_eventrefreshes' table is strictly necessary, or
# whether a stored procedure can be called directly from a cron job. From PoC
# development back in February, I recall that there was no direct method to do
# so, but this may have been before the user permissions issue.
class JobsConfig(AppConfig):
    name = 'jobs'
