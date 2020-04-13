from datetime import date
from typing import List
from mdal.postgres.pg_dto import PGDto


class PGQueryMapper:

    entity: PGDto

    def __init__(self, entity_class: PGDto):
        self.entity = entity_class

    def count(self, **kwargs) -> str:
        return f"SELECT count(*) from {self.get_table()} {self._get_where_clause(**kwargs)};"

    def exists(self, dto: PGDto) -> str:
        properties = dto.get_properties_dict()
        return self.find(**properties)

    def find(self, **kwargs) -> str:
        return f"SELECT * FROM {self.get_table()} {self._get_where_clause(**kwargs)};"

    def save(self, dto: PGDto) -> str:
        property_names = dto.get_property_names()
        return f"INSERT INTO {self.get_table()} ({','.join(property_names)}) VALUES ({('%s,' * len(property_names))[:-1]});"

    def save_all(self, dtos: List[PGDto]) -> str:
        # Currently handled in the abstract dao region, as the common practice is to use the connection
        # object to achieve multi-line insertions in a single call.
        pass

    def delete(self, dto: PGDto):
        properties = dto.get_properties_dict()
        return f"DELETE FROM {self.get_table()} {self._get_where_clause(**properties)};"

    def update(self, dto: PGDto, **kwargs):
        property_names = dto.get_property_names()
        update_property_names = kwargs.keys()

        update_property_string = ",".join([f"{name}=%s" for name in update_property_names])
        property_names_string = " AND ".join([f"{name}=%s" for name in property_names])

        return f"UPDATE {self.get_table()} SET {update_property_string} WHERE {property_names_string};"

    def _get_set_clause(self, **properties):
        if len(properties.keys()) == 0:
            return ""
        else:
            result = [f"{key}='{properties[key]}'" for key in properties]
            return f"{' AND '.join(result)}"

    def _get_where_clause(self, **conditions):
        if len(conditions.keys()) == 0:
            return ""
        else:
            where_conditions = []

            for key in conditions:
                condition = conditions[key]

                if condition is None:
                    continue  # Ignore condition or add "AND key IS NULL"?

                if isinstance(condition, bool):
                    # Boolean, e.g. "key=TRUE"
                    where_conditions.append(f"{key}={'TRUE' if condition else 'FALSE'}")

                elif isinstance(condition, list):

                    if len(condition) == 0:
                        raise Exception(f"Failed to generate the WHERE clause: The list of '{key}' is empty.")

                    elif isinstance(condition[0], float) or isinstance(condition[0], int):
                        # List of numbers, e.g. "key IN (1, 2, 3, 4)"
                        where_conditions.append(f"{key} IN (" + ', '.join(condition) + ")")

                    else:
                        # List of strings, e.g. "key IN ('a', 'b', 'c', 'd')
                        where_conditions.append(f"{key} IN (" + ', '.join([f"'{str(value)}'" for value in condition]) + ")")

                elif isinstance(condition, int) or isinstance(condition, float):
                    # Numerical value, e.g. "key=20"
                    where_conditions.append(f"{key}={condition}")

                elif isinstance(condition, str) or isinstance(condition, date):
                    # String value, e.g. "key='text'"
                    where_conditions.append(f"{key}='{condition}'")

                else:
                    raise Exception(f"WHERE clause does not support conditions for type {str(type(condition))}.")

            return f"WHERE {' AND '.join(where_conditions)}"

    def get_table(self):
        return f"{self.entity.SCHEMA_NAME}.{self.entity.TABLE_NAME}"
