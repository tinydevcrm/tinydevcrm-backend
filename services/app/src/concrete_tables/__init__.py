"""
Concrete tables service.

This Django app manages API endpoints related to managing PostgreSQL tables.
These tables are foreign tables backed by "concrete data", Parquet files
available via 'parquet_fdw' (foreign data wrapper) that serve as the
foundational sources of truth for users. This is opposed to "derived data",
which is data computed via mathematical, logical / relational, or other types of
transformations. For example, a materialized view would be considered "derived
data", while a CSV upload would be considered "concrete data".

Making this distinction guarantees unitary application data flow, and that
consequently, underlying data pipelines are acyclic. This methodology may reduce
likelihood of data corruption via concurrency / paralellism or other concerns,
and helps describe the data model more clearly.

TODO: I'm not terribly sure how to take the complete possible PostgreSQL 'CREATE
TABLE' syntax and translate that through a form. Passing raw SQL queries could
result in security issues. At the same time, not having the ability to template
out the SQL 'CREATE TABLE' syntax may result in much decreased functionality.

TODO: Support table "forking" for alteration of concrete data.

TODO: Create filesystem of users to "shard" foreign tables by user.
"""
