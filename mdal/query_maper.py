from abc import ABC

from mdal.dto import Dto


class QueryMapper(ABC):

    dto: Dto

    def count(self, **kwargs) -> str:
        raise NotImplementedError("Count Query generation is Not Implemented")

    def exists(self, dto: Dto) -> str:
        raise NotImplementedError("Exists Query generation is Not Implemented")

    def find(self, **kwargs) -> str:
        raise NotImplementedError("Find Query generation is Not Implemented")

    def insert(self, dto: Dto) -> str:
        raise NotImplementedError("Insert Query generation is Not Implemented")

    def update(self, dto: Dto, **kwargs):
        raise NotImplementedError("Update Query generation is Not Implemented")

    def upsert(self, dto: Dto, **kwargs):
        raise NotImplementedError("Upsert Query generation is Not Implemented")

    def delete(self, dto: Dto):
        raise NotImplementedError("Delete Query generation is Not Implemented")

    def _get_set_clause(self, **properties):
        raise NotImplementedError("Get Set Clause for Query generation is Not Implemented")

    def _get_where_clause(self, **conditions):
        raise NotImplementedError("Get Where Clause for Query generation is Not Implemented")

    def get_table(self):
        return f"{self.dto.SCHEMA_NAME}.{self.dto.TABLE_NAME}"
