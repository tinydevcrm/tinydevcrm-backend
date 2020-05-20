# Dockerfile to build
#
# A custom Dockerfile is required in order to build 'pg_cron', the data-driven
# colocated job scheduler. Using 'pg_cron' is important for this project to sync
# state between job scheduling and database views with minimal memory and
# complexity footprint.
#
# TODO: Use a non-root user in order to run PostgreSQL.

########## Build `pg_cron` ##########

FROM postgres:12.0-alpine AS pgcron-builder
LABEL application="tinydevcrm-db"

# Install dependencies.
RUN apk add gcc
RUN apk add git
RUN apk add make
RUN apk add musl-dev

# Clone the repository and checkout a specific commit.
RUN git clone https://github.com/tinydevcrm/pg_cron.git /home/pg_cron
# Set work directory.
WORKDIR /home/pg_cron
RUN git checkout 2262d9fadedc9fe0ff16b7690b1d4d95772318cb
# Build 'pg_cron'.
RUN make

########## Build `libarrow` and `parquet_fdw` ##########

FROM python:3.6-alpine AS libarrow-parquetfdw-builder

RUN apk update
RUN apk upgrade
RUN apk add build-base
RUN apk add cmake
RUN apk add bash
RUN apk add boost-dev
RUN apk add autoconf
RUN apk add zlib-dev
RUN apk add libressl-dev
RUN apk add flex
RUN apk add bison

RUN pip install six
RUN pip install pytest
RUN pip install numpy
RUN pip install cython
RUN pip install pandas

ARG ARROW_BUILD_TYPE=release

ENV ARROW_HOME=/usr/local
ENV PARQUET_HOME=/usr/local

WORKDIR /arrow

RUN apk add git

RUN git clone https://github.com/apache/arrow /arrow/arrow
WORKDIR /arrow/arrow

# Checkout 0.17.1
RUN git checkout ff7ee06020949daf66ac05090753e1a17736d9fa
RUN mkdir -p /arrow/arrow/cpp/build

RUN cmake \
    -DCMAKE_BUILD_TYPE=$ARROW_BUILD_TYPE \
    -DOPENSSL_ROOT_DIR=/usr/local/ssl \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_INSTALL_PREFIX=$ARROW_HOME \
    -DARROW_WITH_BZ2=ON \
    -DARROW_WITH_ZLIB=ON \
    -DARROW_WITH_ZSTD=ON \
    -DARROW_WITH_LZ4=ON \
    -DARROW_WITH_SNAPPY=ON \
    -DARROW_PARQUET=ON \
    -DARROW_PYTHON=ON \
    -DARROW_PLASMA=ON \
    -DARROW_BUILD_TESTS=OFF \
    /arrow/arrow/cpp
RUN make -j$(nproc)
RUN make install
RUN cd /arrow/arrow/python && \
    python setup.py build_ext --build-type=$ARROW_BUILD_TYPE --with-parquet \
    && python setup.py install

WORKDIR /parquet_fdw
RUN git clone https://github.com/adjust/parquet_fdw /parquet_fdw/parquet_fdw

# Needed for pg_config
RUN apk add postgresql-dev
WORKDIR /parquet_fdw/parquet_fdw
RUN make
RUN make install

FROM postgres:12.0-alpine AS release
LABEL application="tinydevcrm-db"

# Flatten `make install` commands to reduce build needs.

RUN mkdir -p '/usr/local/lib/postgresql'
RUN mkdir -p '/usr/local/share/postgresql/extension'

# TODO: Might want to change `chown` and not run `postgres` as the default user
# for security purposes.
WORKDIR /home

COPY --from=pgcron-builder /home/pg_cron/pg_cron.so /home/pg_cron.so
COPY --from=pgcron-builder /home/pg_cron/pg_cron.control /home/pg_cron.control
COPY --from=pgcron-builder /home/pg_cron/pg_cron--1.1--1.2.sql /home/pg_cron--1.1--1.2.sql
COPY --from=pgcron-builder /home/pg_cron/pg_cron--1.0--1.1.sql /home/pg_cron--1.0--1.1.sql
COPY --from=pgcron-builder /home/pg_cron/pg_cron--1.0.sql /home/pg_cron--1.0.sql

RUN /usr/bin/install -c -m 755 /home/pg_cron.so '/usr/local/lib/postgresql/pg_cron.so'
RUN /usr/bin/install -c -m 644 /home/pg_cron.control '/usr/local/share/postgresql/extension/'
RUN /usr/bin/install -c -m 644 /home/pg_cron--1.1--1.2.sql '/usr/local/share/postgresql/extension/'
RUN /usr/bin/install -c -m 644 /home/pg_cron--1.0--1.1.sql '/usr/local/share/postgresql/extension/'
RUN /usr/bin/install -c -m 644 /home/pg_cron--1.0.sql '/usr/local/share/postgresql/extension/'


COPY --from=libarrow-parquetfdw-builder /parquet_fdw/parquet_fdw/parquet_fdw.so /home/parquet_fdw.so
COPY --from=libarrow-parquetfdw-builder /parquet_fdw/parquet_fdw/parquet_fdw.control /home/parquet_fdw.control
COPY --from=libarrow-parquetfdw-builder /parquet_fdw/parquet_fdw/parquet_fdw--0.1.sql /home/parquet_fdw--0.1.sql

RUN /usr/bin/install -c -m 755 /home/parquet_fdw.so '/usr/local/lib/postgresql/parquet_fdw.so'
RUN /usr/bin/install -c -m 644 /home/parquet_fdw.control '/usr/local/share/postgresql/extension/'
RUN /usr/bin/install -c -m 644 /home/parquet_fdw--0.1.sql  '/usr/local/share/postgresql/extension/'

RUN rm /home/*

# Copy the script which will initialize the replication permissions
COPY /docker-entrypoint-initdb.d /docker-entrypoint-initdb.d
