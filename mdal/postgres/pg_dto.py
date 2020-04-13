from __future__ import annotations
from abc import ABC


class PGDto(ABC):

    SCHEMA_NAME = None
    TABLE_NAME = None

    @staticmethod
    def from_result_set(result_set: ()) -> PGDto:
        raise NotImplementedError("Mapping from ResultSet is not Implemented.")

    @staticmethod
    def from_json(json_body: str) -> PGDto:
        raise NotImplementedError("Mapping from Json is not Implemented.")

    def get_properties(self):
        return [(key, value) for key, value in self.__dict__.items()
                if not key.startswith("_") and not key.startswith("__")]

    def get_properties_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_") and not key.startswith("__"):
                result[key] = value
        return result

    def get_property_names(self):
        return [key for key, value in self.__dict__.items()
                if not key.startswith("_") and not key.startswith("__")]

    def get_property_values(self):
        return [value for key, value in self.__dict__.items()
                if not key.startswith("_") and not key.startswith("__")]

    def get_representation(self):
        properties = self.get_properties()
        return ", ".join([f"{prop[0]}: {prop[1]}" for prop in properties])

    def __str__(self):
        return f"{type(self).__name__}({self.get_representation()})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if type(self).__name__ != type(other).__name__:
            return False
        try:
            self_properties = self.get_properties_dict()
            other_properties = other.get_properties_dict()

            for key in self_properties.keys():
                if self_properties[key] != other_properties[key]:
                    return False
            return True
        except:
            return False