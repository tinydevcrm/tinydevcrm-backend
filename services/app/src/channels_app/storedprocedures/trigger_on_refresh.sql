-- Create a trigger when an insert occurs into the materialized view refreshes
-- table (currently table name is 'jobs_eventrefreshes'). This trigger should
-- return a JSON payload that matches the newly inserted record.
--
-- This trigger should also expire the record and drop all expired records
-- within the event refreshes table that are older than some amount of time.
-- Currently, this is immediately after expiring the sent record, but this can
-- be extended for preservation purposes.
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
BEGIN
    PERFORM pg_notify('psql_refreshes_channel', NEW.id::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS refreshes_channel ON jobs_eventrefreshes;

CREATE TRIGGER refreshes_channel
    AFTER INSERT OR UPDATE OF status
    ON jobs_eventrefreshes
    FOR EACH ROW
EXECUTE PROCEDURE notify_on_refresh_events_insert();
