# `tinydevcrm-backend` - TinyDevCRM backend / API layer

## Getting Started

Make sure you have the following dependencies, or similar, installed on your
system:

-   `bash`, version 5.0.3(1)-release (x86_64-pc-linux-gnu)
-   `git`, version 2.25.1
-   `docker`, version 19.03.6, build 369ce74a3c
-   `docker-compose`, version 1.23.2, build 1110ad01

This stack was developed against Ubuntu 19.10 Eoan Ermine:

```bash
$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 19.10
Release:        19.10
Codename:       eoan
```

1.  `git` clone this repository:

    ```bash
    git clone https://github.com/yingw787/tinydevcrm-backend
    ```

2.  Run `bash ${DIRNAME}/scripts/setup.sh` to create all Docker builds.

That's it!

Run `${DIRNAME}/scripts/run-dev.sh` to see a development build of TinyDevCRM's API.

Run `${DIRNAME}/scripts/run-prod.sh` to see a production build of TinyDevCRM's API.

## Overview

## For Developers

### Troubleshooting

Sometimes, container processes fail, and the container stops running. To list
Docker containers that are running:

```bash
docker ps
```

To examine the PostgreSQL `db` container's data, run:

```bash
$ docker-compose -f services/docker-compose.development.yaml exec db psql --username=$YOUR_USERNAME --dbname=$YOUR_DATABASE_NAME
```

Use `\l` in order to list all databases, `\c` to select a particular database
and drop into its context, and `\dt` to list all tables within a database. `\q`
to quit `psql`.

To check `docker logs` for a particular container, run:

```bash
docker logs $CONTAINER_NAME
```

Here are some commands in order to run commands for specific containers:

```bash
# Run a migration within the development `docker-compose` context
docker-compose -f services/docker-compose.development.yaml exec web python manage.py migrate --noinput
```
