# Pushpin is a reverse proxying service for realtime communications; use instead
# of having a dedicated message queue or message broker.

FROM fanout/pushpin:1.28.0

# Get package lists, so that if necessary, `docker exec -it pushpin bash` can
# lift into the container and straight up run `apt-get install -y curl` or
# `apt-get install -y telnet` without having to run update first. This should
# not change state of existing packages.
RUN apt-get -y update

COPY pushpin.development.conf /etc/pushpin/pushpin.conf
COPY routes.development /etc/pushpin/routes
