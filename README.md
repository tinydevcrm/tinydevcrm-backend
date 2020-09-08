# `tinydevcrm-backend` - TinyDevCRM backend, including API, DB, and Ops

## System environment assumptions

-   Operating system: Ubuntu 20.04 LTS:

    ```bash
    $ lsb_release -a
    No LSB modules are available.
    Distributor ID: Ubuntu
    Description:    Ubuntu 20.04 LTS
    Release:        20.04
    Codename:       focal
    ```

-   `docker`, Linux container runtime:

    ```bash
    $ docker -v
    Docker version 19.03.8, build afacb8b7f0
    ```

-   `docker-compose`, multi-container single-host Docker runtime addition:

    ```bash
    $ docker-compose -v
    docker-compose version 1.23.2, build 1110ad01
    ```

-   `make`, `Makefile` execution runtime:

    ```bash
    $ make --version
    GNU Make 4.2.1
    Built for x86_64-pc-linux-gnu
    Copyright (C) 1988-2016 Free Software Foundation, Inc.
    License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.
    ```

-   `awscli`, CLI for calling AWS endpoints.

    ```bash
    $ aws --version
    aws-cli/1.18.35 Python/3.7.7 Linux/5.4.0-28-generic botocore/1.15.35
    ```

-   `jq`, JSON parsing utility.

    ```bash
    $ jq --version
    jq-1.6
    ```

## Getting Started

```bash
git clone https://github.com/yingw787/tinydevcrm-backend
cd tinydevcrm-backend
make -f infra-local/Makefile dev-up
```

## Overview

### Running the development environment

To start:

1.  Open a terminal, `cd` into the directory, and run `dev-up`:

    ```bash
    $ cd /path/to/tinydevcrm-backend
    $ make -f infra-dev/Makefile dev-up
    ```

    If an `ipdb` trace appears, enter "c" for "continue", and you should get
    this message:

    ```bash
    /usr/local/lib/python3.8/runpy.py:125: RuntimeWarning: 'ipdb.__main__' found in sys.modules after import of package 'ipdb', but prior to execution of 'ipdb.__main__'; this may result in unpredictable behaviour
    warn(RuntimeWarning(msg))
    > /usr/src/app/manage.py(2)<module>()
        1 #!/usr/bin/env python
    ----> 2 """Django's command-line utility for administrative tasks."""
        3 import os

    ipdb> c
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    June 05, 2020 - 01:25:42
    Django version 3.0.4, using settings 'core.settings'
    Starting ASGI/Channels version 2.4.0 development server at http://0.0.0.0:8000/
    Quit the server with CONTROL-C.
    ```

    Once this message appears, PostgreSQL (database) should be up and running,
    Pushpin (reverse proxy for realtime APIs) should be up and running, and
    Django (web application backend) should be up and running.

    For inspecting an API in the development environment, go to the file you
    want to inspect, and add:

    ```python
    import ipdb
    ipdb.set_trace()
    ```

    And the next time Django runs that code block, it should drop into an `ipdb`
    context within the first (server) terminal window we opened. This should
    live update between the host and the container, as all source files are
    mounted on a Docker volume for instant update between the host and the
    container.

2.  Open a new terminal; this is where we run client queries against the REST
    API.

3.  Create a new user, defined by a primary email and a password.

    ```bash
    curl \
        --header "Content-Type: application/json" \
        --request POST \
        --data '{"primary_email": "me@yingw787.com", "password": "test1234"}' \
        http://localhost:8000/auth/users/register/
    ```

    Primary emails are unique within the system. If you want to differentiate
    between different use cases, and use the same email, use [plus
    addressing](https://www.fastmail.com/help/receive/addressing.html):

    ```bash
    curl \
        --header "Content-Type: application/json" \
        --request POST \
        --data '{"primary_email": "me+specialapp@yingw787.com", "password": "test1234"}' \
        http://localhost:8000/auth/users/register/
    ```

    And the system will register that as a different user. Since plus addressing
    is supported by major email providers, you can configure a folder with the
    same of the alias, any emails from TinyDevCRM should land in that email
    folder with no further action needed on your part.

4.  Obtain a JSON Web Token from the credentials generated by your newly
    registered user, for token-based authentication. This is important to access
    other services from TinyDevCRM, as all services are authenticated.
    Token-based authentication is used here instead of session / cookie-based
    authentication for finer-grained permissioning of API resources.

    ```bash
    curl \
        --header "Content-Type: application/json" \
        --request POST \
        --data '{"primary_email": "me@yingw787.com", "password": "test1234"}' \
        http://localhost:8000/auth/tokens/obtain/
    ```

    You should get this response from the API:

    ```bash
    {"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU5MjUyNjY0MywianRpIjoiNTliOTJjMDdiNDNlNDZlMDk5YjY1ZjhjOWEyMWI1MGMiLCJ1c2VyX2lkIjoxfQ.IkXnAMgIXENQac8t87hAJpzS_nGYdtwDBr04UG8ErwE","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTkxMzE3MzQzLCJqdGkiOiIyZGU5YjE1NWRjZGI0YzU5YWRmZTVkZmM2Y2FjNWMxYSIsInVzZXJfaWQiOjF9.a3ii2l7QgJhDD0527hA5nxDV9EtmbNWcYU8ijDh7wFk"}
    ```

    Token "refresh" is the refresh token. This is the long-lived token that
    validates whether your session is active. Token "access" is the access
    token. This short-lived token is passed to authenticate access to resources.

    If you don't have a software development kit (SDK) or language runtime to
    parse JSON, you can use [`jq`](https://github.com/stedolan/jq) in order to
    parse the JSON response directly from the command line:

    ```bash
    RESPONSE=$(curl --header "Content-Type: application/json" --request POST http://localhost:8000/auth/tokens/obtain/ --data '{"primary_email": "me@yingw787.com", "password": "test1234"}')

    REFRESH=$(echo $RESPNOSE | jq -r ".refresh")
    ACCESS=$(echo $RESPONSE | jq -r ".access")
    ```

    If your access token has expired, TinyDevCRM will return an HTTP 401
    Unauthorized error. Request a new refresh token from the TinyDevCRM API
    before continuing to proceed:

    ```bash
    curl \
        --header "Content-Type: application/json" \
        --request POST \
        --data '{"refresh": "$YOUR_JWT_REFRESH_TOKEN"}' \
        http://localhost:8000/auth/tokens/refresh/
    ```

    If you wish to log out of your session, blacklist the refresh token using
    the TinyDevCRM API and all requests with that refresh token (and any access
    tokens generated from it) will not pass authentication:

    ```bash
    curl \
        --header "Content-Type: application/json" \
        --request POST \
        --data '{"refresh": "$YOUR_JWT_REFRESH_TOKEN"}' \
        http://localhost:8000/auth/tokens/blacklist/
    ```

5.  Create a table, by specifying column definitions and uploading an Apache
    Parquet file to fit some data. Parquet is used for data integrity purposes.

    In order to create an Apache Parquet file from a CSV file, you can download
    [`conda`](https://docs.conda.io/en/latest/), and with it,
    [`pandas`](https://anaconda.org/anaconda/pandas) and
    [`pyarrow`](https://anaconda.org/conda-forge/pyarrow):

    ```bash
    # Create a conda environment
    $ conda create -n myenv python=3.8
    $ conda activate myenv
    (myenv) $ conda install pandas
    (myenv) $ conda install pyarrow
    ```

    Open a Python shell and run the following statement:

    ```python
    import pandas as pd

    pd.read_csv('/path/to/file.csv').to_parquet('/path/to/file.parquet')
    ```

    As an example, [`sample.parquet`](sample.parquet), is generated from
    [`sample.csv`](sample.csv) using this method.

    Then, create the table:

    ```bash
    curl \
        --header "Content-Type: multipart/form-data" \
        --header "Authorization: JWT $YOUR_JWT_ACCESS_TOKEN" \
        --request POST \
        --form "file=@/path/to/file.parquet" \
        --form "table_name=$YOUR_TABLE_NAME" \
        --form columns='[{"column_name": "SomeNumber", "column_type":"int"},{"column_name":"SomeString","column_type":"varchar(256)"}]' \
        http://localhost:8000/tables/create/
    ```

6.  Create a materialized view, which caches a specific SQL query you want to
    execute against your table (or tables, if you have multiple and want to
    execute joins):

    ```bash
    curl \
        --header "Content-Type: application/json" \
        --header "Authorization: JWT $YOUR_JWT_ACCESS_TOKEN" \
        --request POST \
        --data '{"view_name": "$YOUR_VIEW_NAME", "sql_query": "SELECT * FROM $YOUR_TABLE_NAME WHERE \"SomeNumber\" = CAST( EXTRACT( SECOND FROM NOW()) * 1000000 AS INTEGER) % 10"}' \
        http://localhost:8000/views/create/
    ```

    You can pass any single SQL statement, provided that it starts with
    'SELECT', 'TABLES', or 'VALUES' (i.e. is read-only).

7.  Create a cron job. This refreshes the materialized view in order to fetch
    updated information from the underlying table, at a frequency for your
    choosing.

    ```bash
    curl \
        --header "Content-Type: application/json" \
        --header "Authorization: JWT $YOUR_JWT_ACCESS_TOKEN" \
        --request POST \
        --data '{"view_name": "$YOUR_VIEW_NAME", "crontab_def": "* * * * *"}' \
        http://localhost:8000/jobs/create/
    ```

    See [Crontab Guru](https://crontab.guru/) for an example of how to configure
    cron jobs. TinyDevCRM supports materialized view refreshes on a per-minute
    granularity.

8.  Create a channel to listen for refresh events on the materialized view, via
    HTTP/2 and Server-Sent Events:

    ```bash
    curl \
        --header "Content-Type: application/json" \
        --header "Authorization: JWT $YOUR_JWT_ACCESS_TOKEN" \
        --request POST \
        --data '{"job_id": "$YOUR_JOB_ID"}' \
        http://localhost:8000/channels/create/
    ```

    This should return a UUID representing the channel's public identifier.

9.  Listen to the channel; this process should run forever.

    ```bash
    curl \
        --header "Content-Type: application/json" \
        --header "Authorization: JWT $ACCESS" \
        --request GET \
        http://localhost:7999/channels/$YOUR_CHANNEL_UUID/listen/
    ```

### Miscellaneous development commands

In order to log into the development PostgreSQL instance, run:

```bash
make -f infra-dev/Makefile dev-psql
```

### Running the production environment

To start the production cluster:

```bash
make -f infra-prod/Makefile prod-up
```

To teardown the production cluster:

```bash
make -f infra-prod/Makefile prod-down
```

### Miscellaneous production commands

To see the templated `docker-compose.aws.yaml` configuration file (important for
building the correct Docker images to ship to ECR):

```bash
make -f infra-prod/Makefile prod-config
```

To log into the production PostgreSQL instance, run:

```bash
make -f infra-prod/Makefile prod-psql
```

### Creating the AWS stack

Look at `infra-aws/SETUP.md` for more details.

## Changelog

See [CHANGELOG](docs/CHANGELOG.md) for additional details.

## Roadmap

See [ROADMAP](docs/ROADMAP.md) for additional details.

## License

See [LICENSE](LICENSE) for additional details.
