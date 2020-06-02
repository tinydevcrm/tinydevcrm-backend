# Pushpin is a reverse proxying service for realtime communications; use instead
# of having a dedicated message queue or message broker.

FROM fanout/pushpin:1.28.0

COPY pushpin.development.conf /etc/pushpin/pushpin.conf
