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

## Getting Started

```bash
git clone https://github.com/yingw787/tinydevcrm-backend
cd tinydevcrm-backend
make -f infra-local/Makefile run-dev
```

## Overview

## Features

-   Token-based authentication using JSON Web Tokens
-   API-first backend using Django REST Framework
-   Local operations using Docker and `docker-compose`.
-   Cloud-based operations using AWS
