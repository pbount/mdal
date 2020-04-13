from abc import ABC

from mdal.query_maper import QueryMapper


class Dao(ABC):

    _query_mapper: QueryMapper

    def count(self, **kwargs) -> int:
        raise NotImplementedError("Count function is Not Implemented")

    def exists(self, dto) -> bool:
        raise NotImplementedError("Exists function is Not Implemented")

    def find(self, **kwargs):
        raise NotImplementedError("Find function is Not Implemented")

    def find_one(self, **kwargs):
        raise NotImplementedError("Find One function is Not Implemented")

    def insert(self, dtos):
        raise NotImplementedError("Insert function is Not Implemented")

    def update(self, dto, **kwargs):
        raise NotImplementedError("Update function is Not Implemented")

    def upsert(self, dtos):
        raise NotImplementedError("Upsert function is Not Implemented")

    def delete(self, dto):
        raise NotImplementedError("Delete function is Not Implemented")

    def __execute_read(self, sql: str):
        raise NotImplementedError("Execute Read query is Not Implemented")

    def __execute_read_dict(self, sql: str):
        raise NotImplementedError("Execute read dict query is Not Implemented")

    def __execute_write(self, sql: str, values: () = None):
        raise NotImplementedError("Execute write query is Not Implemented")
