from typing import Any
from mdal.dao import Dao
from mdal.postgres.pg_query_mapper import PGQueryMapper


class PGDao(Dao):

    _query_mapper: PGQueryMapper
    connection: Any

    def __init__(self, entity_class, connection, cursor_factory=None):
        self.entity_class = entity_class
        self.connection = connection
        self._query_mapper = PGQueryMapper(entity_class)
        self.cursor_factory = cursor_factory

    def count(self, **kwargs) -> int:
        count_query = self._query_mapper.count(**kwargs)
        count_result = self.__execute_read(count_query)

        return count_result[0][0]

    def exists(self, dto) -> bool:
        exists_query = self._query_mapper.exists(dto)
        find_result_set = self.__execute_read(exists_query)

        return len(find_result_set) > 0

    def find(self, **kwargs):
        find_query = self._query_mapper.find(**kwargs)
        find_result_set = self.__execute_read_dict(find_query)
        mapped_results = [self.entity_class.from_result_set(find_result) for find_result in find_result_set]
        return mapped_results

    def find_one(self, **kwargs):
        results = self.find(**kwargs)

        if len(results) == 0:
            raise Exception("One Result Expected, None found.")

        if len(results) > 1:
            raise Exception(f"One Result Expected, {len(results)} found.")

        return results[0]

    def insert(self, dtos):
        if type(dtos) is list:
            # TODO: Find a way to produce a multi-insertion query without relying on the cursor, or, pass the cursor
            #  inside the query mapper.
            cursor = self.connection.cursor()
            query = cursor.mogrify("INSERT INTO {} ({}) VALUES {};".format(
                f"{dtos[0].SCHEMA_NAME}.{dtos[0].TABLE_NAME}",
                ', '.join(dtos[0].get_property_names()),
                ', '.join(['%s'] * len(dtos))
            ), [tuple(dto.get_property_values()) for dto in dtos])
            self.__execute_write(query)
        else:
            save_query = self._query_mapper.save(dtos)
            self.__execute_write(save_query, dtos.get_property_values())

    def update(self, dto, **kwargs):
        update_query = self._query_mapper.update(dto, **kwargs)
        values = tuple(kwargs.values()) + tuple(dto.get_property_values())
        self.__execute_write(update_query, values)

    def upsert(self, dtos):
        # TODO: Find a way to produce a multi-insertion query without relying on the cursor, or, pass the cursor
        #  inside the query mapper.
        if type(dtos) is not list:
            dtos = [dtos]

        cursor = self.connection.cursor()
        schema_table = f"{dtos[0].SCHEMA_NAME}.{dtos[0].TABLE_NAME}"
        property_names = ', '.join(dtos[0].get_property_names())
        property_values = ', '.join(['%s'] * len(dtos))
        table_pkey = f"{dtos[0].TABLE_NAME}_pkey"
        fields_to_update = ', '.join([f"{name}=EXCLUDED.{name}" for name in dtos[0].get_property_names()])

        query = "INSERT INTO {} ({}) VALUES {} ON CONFLICT ON CONSTRAINT {} DO UPDATE SET {};".format(
            schema_table,
            property_names,
            property_values,
            table_pkey,
            fields_to_update
        )

        values = [tuple(dto.get_property_values()) for dto in dtos]

        query_and_values = cursor.mogrify(query, values)
        self.__execute_write(query_and_values)

    def delete(self, dto):
        delete_query = self._query_mapper.delete(dto)
        self.__execute_write(delete_query)

    def __execute_read(self, sql: str):
        cursor = self.connection.cursor()
        cursor.execute(sql)

        return cursor.fetchall()

    def __execute_read_dict(self, sql: str):
        if self.cursor_factory:
            cursor = self.connection.cursor(cursor_factory=self.cursor_factory)
        else:
            cursor = self.connection.cursor()
        cursor.execute(sql)

        return cursor.fetchall()

    def __execute_write(self, sql: str, values: () = None):
        cursor = self.connection.cursor()
        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        self.connection.commit()