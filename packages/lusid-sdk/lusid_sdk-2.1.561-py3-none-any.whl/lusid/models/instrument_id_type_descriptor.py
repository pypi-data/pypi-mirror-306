# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict
from pydantic.v1 import BaseModel, Field, StrictBool, StrictStr, constr

class InstrumentIdTypeDescriptor(BaseModel):
    """
    The description of an allowable instrument identifier.  # noqa: E501
    """
    identifier_type: constr(strict=True, min_length=1) = Field(..., alias="identifierType", description="The name of the identifier type.")
    property_key: StrictStr = Field(..., alias="propertyKey", description="The property key that corresponds to the identifier type.")
    is_unique_identifier_type: StrictBool = Field(..., alias="isUniqueIdentifierType", description="Whether or not the identifier type is enforced to be unique.")
    __properties = ["identifierType", "propertyKey", "isUniqueIdentifierType"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> InstrumentIdTypeDescriptor:
        """Create an instance of InstrumentIdTypeDescriptor from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> InstrumentIdTypeDescriptor:
        """Create an instance of InstrumentIdTypeDescriptor from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return InstrumentIdTypeDescriptor.parse_obj(obj)

        _obj = InstrumentIdTypeDescriptor.parse_obj({
            "identifier_type": obj.get("identifierType"),
            "property_key": obj.get("propertyKey"),
            "is_unique_identifier_type": obj.get("isUniqueIdentifierType")
        })
        return _obj
