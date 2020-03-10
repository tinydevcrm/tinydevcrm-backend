# Dockerfile to reproducibly build applications.
FROM ubuntu:19.10

# Set environment variables for Docker build process.
ARG DEBIAN_FRONTEND=noninteractive

# Install process-wide dependencies.
RUN apt-get -y update
RUN apt-get -y upgrade

ENTRYPOINT [ "/app/entrypoint.sh" ]
