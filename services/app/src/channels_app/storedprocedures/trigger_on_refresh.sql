-- Create a trigger when an insert occurs into the materialized view refreshes
-- table (currently table name is 'jobs_eventrefreshes'). This trigger should
-- return a JSON payload that matches the newly inserted record.
--
-- This trigger should also expire the record and drop all expired records
-- within the event refreshes table that are older than some amount of time.
-- Ideally, this is immediately after expiring the sent record. This logic can
-- be extended for preservation purposes.
--
-- TODO: This file is *extremely* sensitive to changes in the Django
-- jobs/models.py EventRefreshes() model. I wonder whether there's a way to get
-- ORM-like functionality within PostgreSQL, maybe by using PL/Python (?).
--
-- TODO: If necessary, template this file out, make a copy, and replace template
-- parameters with user-defined parameters. This shouldn't be necessary since
-- multi-host is not used, and ZMQ pub/sub isn't used either, so there is no way
-- to connect multiple database channels to the reverse proxy directly, which
-- necessitates using the webapp.
--
-- Inspired by: https://layerci.com/blog/postgres-is-the-answer/
CREATE OR REPLACE FUNCTION notify_on_refresh_events_insert()
    RETURNS trigger AS
$$
DECLARE
    payload TEXT;
BEGIN
    -- Convert the inserted row into a JSON payload. See:
    -- https://gist.github.com/colophonemes/9701b906c5be572a40a84b08f4d2fa4e
    -- (bottom of the comment thread) and
    -- https://www.postgresql.org/docs/12/functions-json.html
    payload := row_to_json(NEW)::TEXT;

    -- Broadcast the inserted row as data. Any new information sent out by the
    -- PostgreSQL channel should be updated as part of the Django
    -- 'jobs_eventrefreshes' table.
    PERFORM pg_notify('psql_refreshes_channel', payload);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS refreshes_channel ON jobs_eventrefreshes;
CREATE TRIGGER refreshes_channel
    AFTER INSERT
    ON jobs_eventrefreshes
    FOR EACH ROW
EXECUTE PROCEDURE notify_on_refresh_events_insert();


CREATE OR REPLACE FUNCTION delete_old_rows()
    RETURNS trigger AS
$$
BEGIN
    -- Delete from the table all records that are older than 1 hour:
    -- https://www.the-art-of-web.com/sql/trigger-delete-old/
    --
    -- TODO: Flush old logs to a backup store somewhere instead.
    DELETE FROM jobs_eventrefreshes WHERE created < NOW() - INTERVAL '1 hour';
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS delete_old_rows_from_view_refreshes ON jobs_eventrefreshes;
CREATE TRIGGER delete_old_rows_from_view_refreshes
    AFTER INSERT OR UPDATE OF status
    ON jobs_eventrefreshes
    FOR EACH ROW
EXECUTE PROCEDURE delete_old_rows();
