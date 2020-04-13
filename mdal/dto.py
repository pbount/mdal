from __future__ import annotations
from abc import ABC


class Dto(ABC):

    SCHEMA_NAME = None
    TABLE_NAME = None

    @staticmethod
    def from_result_set(result_set: ()) -> Dto:
        raise NotImplementedError("Mapping from ResultSet is not Implemented.")

    @staticmethod
    def from_json(json_body: str) -> Dto:
        raise NotImplementedError("Mapping from Json is not Implemented.")

    def get_properties(self):
        raise NotImplementedError("Getting properties from Dto is not implemented")

    def get_properties_dict(self):
        raise NotImplementedError("Getting properties dictionary from Dto is not implemented")

    def get_property_names(self):
        raise NotImplementedError("Getting property names from Dto is not implemented")

    def get_property_values(self):
        raise NotImplementedError("Getting property Values from Dto is not implemented")

    def get_representation(self):
        raise NotImplementedError("Getting String representation of Dto is not implemented")
