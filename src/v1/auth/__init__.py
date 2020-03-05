"""
V1 authentication service.

NOTE: I abstracted this out as its own service, since it has its own models and
its own migrations it needs to maintain (e.g. a table of blacklisted JWT
tokens). It's also a learning experience in how Django namespaces API endpoints.
"""
