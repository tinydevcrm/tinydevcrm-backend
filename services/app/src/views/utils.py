"""
Utility classes, methods, and variables for views service.

PostgreSQL enum type declaration:
https://schinckel.net/2019/09/18/postgres-enum-types-in-django/
"""

import psycopg2
from psycopg2.extensions import (
    new_array_type,
    new_type,
    QuotedString,
    register_adapter,
    register_type,
)
known_types = set()


CREATE_TYPE = 'CREATE TYPE {0} AS ENUM ({1})'
SELECT_OIDS = 'SELECT %s::regtype::oid AS "oid", %s::regtype::oid AS "array_oid"'


class register_enum(object):
    def __init__(self, db_type, managed=True):
        self.db_type = db_type
        self.array_type = '{}[]'.format(db_type)
        self.managed = managed

    def __call__(self, cls):
        # Tell psycopg2 how to turn values of this class into db-ready values.
        register_adapter(cls, lambda value: QuotedString(value.value))

        # Store a reference to this instance's "register" method, which allows
        # us to do the magic to turn database values into this enum type.
        known_types.add(self.register)

        self.values = [
            member.value
            for member in cls.__members__.values()
        ]

        # We need to keep a reference to the new class around, so we can use it later.
        self.cls = cls

        return cls

    def register(self, connection):
        with connection.cursor() as cursor:
            try:
                cursor.execute(SELECT_OIDS, [self.db_type, self.array_type])
                oid, array_oid = cursor.fetchone()
            except psycopg2.ProgrammingError:
                if self.managed:
                    cursor.execute(self.create_enum(connection), self.values)
                else:
                    return

        custom_type = new_type(
            (oid,),
            self.db_type,
            lambda data, cursor: data and self.cls(data) or None
        )
        custom_array = new_array_type(
            (array_oid,),
            self.array_type,
            custom_type
        )
        register_type(custom_type, cursor.connection)
        register_type(custom_array, cursor.connection)

    def create_enum(self, connection):
        qn = connection.ops.quote_name
        return CREATE_TYPE.format(
            qn(self.db_type),
            ', '.join(['%s' for value in self.values])
        )
