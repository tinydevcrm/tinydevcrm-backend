"""
Channels service.

This Django app creates a channel where events are placed after generation. For
example, a cron job generating a materialized view refresh can send an event on
a specific channel, which a client 'curl'ing that particular channel can listen
to.

This service leverages HTTP/2 and Server Sent Events (SSE) as an HTTP-based,
unidirectional event-driven dataflow.
"""
