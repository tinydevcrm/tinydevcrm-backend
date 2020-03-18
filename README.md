# `api.tinydevcrm.com` - TinyDevCRM backend / API layer

## Getting Started

Make sure you have the following dependencies installed on your system:

-   `bash`, version 5.0.3(1)-release (x86_64-pc-linux-gnu)
-   `git`, version 2.25.1
-   `docker`, version 19.03.6, build 369ce74a3c
-   `docker-compose`, version 1.23.2, build 1110ad01

I'm using Ubuntu 19.10 Eoan Ermine:

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
    git clone https://github.com/yingw787/api.tinydevcrm.com ${DIRNAME}/
    ```

2.  Run `bash ${DIRNAME}/scripts/setup.sh` to create all Docker builds.

That's it!

Run `${DIRNAME}/scripts/run-dev.sh` to see a development build of TinyDevCRM's API.

Run `${DIRNAME}/scripts/run-prod.sh` to see a production build of TinyDevCRM's API.

## Overview

## For Developers
