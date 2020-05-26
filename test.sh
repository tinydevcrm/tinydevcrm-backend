#!/bin/bash

# Register a new test user.
curl --header "Content-Type: application/json" -X POST http://localhost:8000/auth/users/register/ --data '{"primary_email": "me@yingw787.com", "password": "test1234"}' || true

# Obtain a JSON web token.
RESPONSE=$(curl --header "Content-Type: application/json" -X POST http://localhost:8000/auth/tokens/obtain/ --data '{"primary_email": "me@yingw787.com", "password": "test1234"}')

echo "Response is: " $RESPONSE

REFRESH=$(echo $RESPNOSE | jq -r ".refresh")
ACCESS=$(echo $RESPONSE | jq -r ".access")

echo "Refresh is: " $REFRESH
echo "Access is: " $ACCESS

# Upload a Parquet file to server to create a PostgreSQL foreign table.
curl --header "Content-Type: multipart/form-data" --header "Authorization: JWT $ACCESS" -X POST  -F file=@sample.parquet -F table_name=sample_table -F columns='[{"column_name": "SomeNumber", "column_type":"int"},{"column_name":"SomeString","column_type":"varchar(256)"}]' http://localhost:8000/tables/create/

# Create materialized view.
curl --header "Content-Type: application/json" --header "Authorization: JWT $ACCESS" -X POST --data '{"view_name": "sample_view", "sql_query": "SELECT * FROM sample_table"}' http://localhost:8000/views/create/

# Create scheduled job.
JOB_RESPONSE=$(curl --header "Content-Type: application/json" --header "Authorization: JWT $ACCESS" -X POST --data '{"view_name": "sample_view", "crontab_def": "* * * * *"}' http://localhost:8000/jobs/create/)

CRON_JOB_ID=1

# Issue event on pub/sub upon insert into_table refresh view event.
curl --header "Content-Type: application/json" --header "Authorization: JWT $ACCESS" -X POST --data '{"job_id": "${CRON_JOB_ID}"}' http://localhost:8000/channels/create/

# Create materialized view refreshes table to store job scheduler events. Should
# be done as part of a migration. DONE

# Refresh materialized view. DONE

# Register materialized view with 'pg_cron' and insert materialized view into
# refreshes table (good to separate out whether or not a refresh is active) DONE
