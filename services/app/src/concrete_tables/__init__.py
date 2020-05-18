"""
Concrete tables service.

This Django app pre-creates PostgreSQL tables for ingestion of "concrete data".
This way, no expensive type inference needs to be run on the data, and usage of
the native PostgreSQL COPY FROM tool can be leveraged in lieu of building a
custom RFC-4180 compliant CSV parser.

TODO: I'm not terribly sure how to take the complete possible PostgreSQL 'CREATE
TABLE' syntax and translate that through a form. Passing raw SQL queries could
result in security issues. At the same time, not having the ability to template
out the SQL 'CREATE TABLE' syntax may result in much decreased functionality.
"""
