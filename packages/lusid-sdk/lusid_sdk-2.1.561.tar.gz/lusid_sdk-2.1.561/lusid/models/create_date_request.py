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

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic.v1 import BaseModel, Field, StrictStr, constr, validator
from lusid.models.date_attributes import DateAttributes

class CreateDateRequest(BaseModel):
    """
    CreateDateRequest
    """
    date_id: constr(strict=True, max_length=256, min_length=1) = Field(..., alias="dateId")
    from_utc: datetime = Field(..., alias="fromUtc")
    to_utc: datetime = Field(..., alias="toUtc")
    time_zone: constr(strict=True, max_length=5, min_length=0) = Field(..., alias="timeZone")
    description: constr(strict=True, max_length=100, min_length=0) = Field(...)
    type: Optional[constr(strict=True, max_length=10, min_length=0)] = None
    attributes: Optional[DateAttributes] = None
    source_data: Optional[Dict[str, StrictStr]] = Field(None, alias="sourceData")
    __properties = ["dateId", "fromUtc", "toUtc", "timeZone", "description", "type", "attributes", "sourceData"]

    @validator('date_id')
    def date_id_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[a-zA-Z0-9\-_]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_]+$/")
        return value

    @validator('time_zone')
    def time_zone_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[a-zA-Z0-9\-_]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_]+$/")
        return value

    @validator('description')
    def description_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[\s\S]*$", value):
            raise ValueError(r"must validate the regular expression /^[\s\S]*$/")
        return value

    @validator('type')
    def type_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[a-zA-Z0-9\-_]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_]+$/")
        return value

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
    def from_json(cls, json_str: str) -> CreateDateRequest:
        """Create an instance of CreateDateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of attributes
        if self.attributes:
            _dict['attributes'] = self.attributes.to_dict()
        # set to None if type (nullable) is None
        # and __fields_set__ contains the field
        if self.type is None and "type" in self.__fields_set__:
            _dict['type'] = None

        # set to None if source_data (nullable) is None
        # and __fields_set__ contains the field
        if self.source_data is None and "source_data" in self.__fields_set__:
            _dict['sourceData'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CreateDateRequest:
        """Create an instance of CreateDateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CreateDateRequest.parse_obj(obj)

        _obj = CreateDateRequest.parse_obj({
            "date_id": obj.get("dateId"),
            "from_utc": obj.get("fromUtc"),
            "to_utc": obj.get("toUtc"),
            "time_zone": obj.get("timeZone"),
            "description": obj.get("description"),
            "type": obj.get("type"),
            "attributes": DateAttributes.from_dict(obj.get("attributes")) if obj.get("attributes") is not None else None,
            "source_data": obj.get("sourceData")
        })
        return _obj
