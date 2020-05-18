#!/bin/bash

# Register a new test user.
curl --header "Content-Type: application/json" -X POST http://localhost:8000/v1/auth/users/register/ --data '{"primary_email": "me@yingw787.com", "password": "test1234"}' || true

# Obtain a JSON web token.
RESPONSE=$(curl --header "Content-Type: application/json" -X POST http://localhost:8000/v1/auth/tokens/obtain/ --data '{"primary_email": "me@yingw787.com", "password": "test1234"}')

echo "Response is: " $RESPONSE

REFRESH=$(echo $RESPNOSE | jq -r ".refresh")
ACCESS=$(echo $RESPONSE | jq -r ".access")

echo "Refresh is: " $REFRESH
echo "Access is: " $ACCESS

# Test that things are working.
curl --header "Content-Type: application/json" --header "Authorization: JWT $ACCESS" -X GET http://localhost:8000/v1/data/test/

# Create a PostgreSQL table.

curl --header "Content-Type: application/json" --header "Authorization: JWT $ACCESS" -X POST --data '{"name": "some_table", "dry_run": "1", "columns": [{"name": "columnA", "type": "nvarchar(256)"}, {"name": "columnB", "type": "bytea"}]}' http://localhost:8000/v1/tables/create/

# # Upload a CSV file to remote.
# curl --header "Content-Type: multipart/form-data" --header "Authorization: JWT $ACCESS" -X POST  -F file=@sample.csv http://localhost:8000/v1/data/upload/

# Create materialized view.

# Refresh materialized view.

# Create materialized view refreshes table to store job scheduler events.

# Register materialized view with 'pg_cron' and insert materialized view into
# refreshes table (good to separate out whether or not a refresh is active)

# Issue event on pub/sub upon insert into_table refresh view event.
