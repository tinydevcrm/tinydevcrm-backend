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

echo "Job response is: " $JOB_RESPONSE

# IMPORTANT use jq in order to create a new JSON dict, cast value to string
CHANNEL_REQUEST_DATA=$(echo $JOB_RESPONSE | jq '{job_id: .job_id|tostring}')

echo "Channel request data is: " $CHANNEL_REQUEST_DATA

# Create channel to listen to one specific cron job.
# IMPORTANT wrap data in double quotes in order to preserve bash variables,
# doesn't matter that internal variables are double quoted as well
CHANNELS_RESPONSE=$(curl --header "Content-Type: application/json" --header "Authorization: JWT $ACCESS" -X POST --data "$CHANNEL_REQUEST_DATA" http://localhost:8000/channels/create/)

CHANNEL_ID=$(echo $CHANNELS_RESPONSE | jq -r ".public_identifier")

echo "Channel ID is: " $CHANNEL_ID

# TODO: Open channel for cron job refreshes.
echo "Run this command in order to test channel: " "curl --header \"Content-Type: application/json\" --header \"Authorization: JWT $ACCESS\" -X POST http://localhost:8000/channels/$CHANNEL_ID/open/"

# Listen to channel for cron job refreshes. THIS WORKS RIGHT NOW BUT TAKES UP THE FULL TERMINAL, RUN IN A SEPARATE TERMINAL
echo "Run this command in order to listen to channel: " "curl --header \"Content-Type: application/json\" --header \"Authorization: JWT $ACCESS\" -X GET http://localhost:8000/channels/$CHANNEL_ID/listen/"

# Close channel.
echo "Run this commmand in order to close channel: " "curl --header \"Content-Type: application/json\" --header \"Authorization: JWT $ACCESS\" -X POST http://localhost:8000/channels/$CHANNEL_ID/close/"

# TODO: Create materialized view refreshes table to store job scheduler events.
# Should be done as part of a migration.

# TODO: Refresh materialized view.

# TODO: Register materialized view with 'pg_cron' and insert materialized view
# into refreshes table (good to separate out whether or not a refresh is active)
