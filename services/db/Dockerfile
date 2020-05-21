# This Dockerfile builds 'pg_cron', the data-driven job scheduler, colocated
# with PostgreSQL. Using 'pg_cron' is important for this project to sync state
# between job scheduling and database views with minimal memory and complexity
# footprint.
#
# This Dockerfile also builds `parquet_fdw`, which enables PostgreSQL to
# leverage imported Parquet files to create foreign tables.
#
# TODO: Use a non-root user in order to run PostgreSQL.

FROM postgres:12.3
LABEL application="tinydevcrm-db"

# Update.
RUN apt-get -y update
RUN apt-get -y upgrade

########## START 'pg_cron' ##########

# Install dependencies.
RUN apt-get install -y build-essential
RUN apt-get install -y git
RUN apt-get install -y postgresql-server-dev-12

# Clone the repository and checkout a specific commit.
RUN git clone https://github.com/tinydevcrm/pg_cron.git /home/pg_cron
# Set work directory.
WORKDIR /home/pg_cron
RUN git checkout 2262d9fadedc9fe0ff16b7690b1d4d95772318cb
# Build and install 'pg_cron'.
RUN make
RUN make install

# Remove source deps.
WORKDIR /home
RUN rm -rf /home/pg_cron

# Remove all previous build dependencies.
RUN apt-get remove -y build-essential
RUN apt-get remove -y git
RUN apt-get remove -y postgresql-server-dev-12

########## END 'pg_cron' ##########

########## START 'parquet_fdw' ##########

# Install dependencies.

# Install Apache Arrow #
RUN apt-get -y install lsb-release
RUN apt-get -y install wget

# Set up package archives for distro version #
RUN if [ $(lsb_release --codename --short) = "stretch" ]; then tee /etc/apt/sources.list.d/backports.list <<APT_LINE; deb http://deb.debian.org/debian $(lsb_release --codename --short)-backports main; APT_LINE; fi
RUN wget https://apache.bintray.com/arrow/$(lsb_release --id --short | tr 'A-Z' 'a-z')/apache-arrow-archive-keyring-latest-$(lsb_release --codename --short).deb
RUN apt-get -y install ./apache-arrow-archive-keyring-latest-$(lsb_release --codename --short).deb
RUN apt-get -y update

RUN apt-get -y install libarrow-dev
RUN apt-get -y install libarrow-glib-dev
RUN apt-get -y install libparquet-dev
RUN apt-get -y install libparquet-glib-dev

# Install `parquet_fdw` #
RUN apt-get install -y git
RUN apt-get install -y postgresql-server-dev-12

RUN git clone https://github.com/tinydevcrm/parquet_fdw.git /home/parquet_fdw
# Set work directory.
WORKDIR /home/parquet_fdw
RUN git checkout 0cc795d2811891056842ac82f97da35998cc3ec4
# Build and install 'parquet_fdw'.
RUN make
RUN make install

# Remove all previous build dependencies.
RUN apt-get remove -y lsb-release
RUN apt-get remove -y wget
RUN apt-get remove -y git
RUN apt-get remove -y postgresql-server-dev-12
RUN apt-get remove -y libarrow-dev
RUN apt-get remove -y libarrow-glib-dev
RUN apt-get remove -y libparquet-dev
RUN apt-get remove -y libparquet-glib-dev

########## END 'parquet_fdw' ##########

# Copy the script which will initialize the replication permissions
COPY /docker-entrypoint-initdb.d /docker-entrypoint-initdb.d
