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
from typing import Any, Dict, Optional, Union
from pydantic.v1 import BaseModel, Field, StrictFloat, StrictInt, StrictStr

class PerformanceReturn(BaseModel):
    """
    A list of Returns.  # noqa: E501
    """
    effective_at: datetime = Field(..., alias="effectiveAt", description="The effectiveAt for the return.")
    rate_of_return: Union[StrictFloat, StrictInt] = Field(..., alias="rateOfReturn", description="The return number.")
    opening_market_value: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="openingMarketValue", description="The opening market value.")
    closing_market_value: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="closingMarketValue", description="The closing market value.")
    period: Optional[StrictStr] = Field(None, description="Upsert the returns on a Daily or Monthly period. Defaults to Daily.")
    __properties = ["effectiveAt", "rateOfReturn", "openingMarketValue", "closingMarketValue", "period"]

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
    def from_json(cls, json_str: str) -> PerformanceReturn:
        """Create an instance of PerformanceReturn from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if opening_market_value (nullable) is None
        # and __fields_set__ contains the field
        if self.opening_market_value is None and "opening_market_value" in self.__fields_set__:
            _dict['openingMarketValue'] = None

        # set to None if closing_market_value (nullable) is None
        # and __fields_set__ contains the field
        if self.closing_market_value is None and "closing_market_value" in self.__fields_set__:
            _dict['closingMarketValue'] = None

        # set to None if period (nullable) is None
        # and __fields_set__ contains the field
        if self.period is None and "period" in self.__fields_set__:
            _dict['period'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PerformanceReturn:
        """Create an instance of PerformanceReturn from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PerformanceReturn.parse_obj(obj)

        _obj = PerformanceReturn.parse_obj({
            "effective_at": obj.get("effectiveAt"),
            "rate_of_return": obj.get("rateOfReturn"),
            "opening_market_value": obj.get("openingMarketValue"),
            "closing_market_value": obj.get("closingMarketValue"),
            "period": obj.get("period")
        })
        return _obj
