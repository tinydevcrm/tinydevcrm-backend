"""
Events service.

This Django app handles API endpoints for defining JSON packages emitted via
pub/sub.

TODO: Figure out a way to maintain persistent connections on a per-user or a
per-agent basis. According to this Stack Overflow answer
(https://stackoverflow.com/a/22714018), opening tens of millions of TCP
connections shouldn't be a problem for a server. Keeping concurrent TCP
connections is much harder (since the number of TCP ports per server hovers
somewhere around 65,535). Multiplexing requests on a single channel isn't ideal,
since everybody can see each other's messages and additional security
requirements likely need to be implemented for production usage, but I don't yet
have the knowledge to handle web-scale, independent pub/sub.
"""
