"""
Views service.

This Django app manages API endpoints related to managing PostgreSQL
materialized views. These views match to certain PostgreSQL tables via
customizable SQL query, so that view refreshing will bring up a certain set of
data depending on conditions changing with time.

This enables different windows into an existing pool of data, and leverages
PostgreSQL's native caching ability (if any) that's colocated with the data.
"""
