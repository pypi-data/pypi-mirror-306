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
from pydantic.v1 import BaseModel, Field, StrictFloat, StrictInt

class BondConversionEntry(BaseModel):
    """
    Information required to specify a conversion event for a convertible bond.  # noqa: E501
    """
    var_date: Optional[datetime] = Field(None, alias="date", description="The date at which the bond can be converted")
    denomination: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="The number of shares to be issued on conversion will be equal to the denomination of the  bond divided by the conversion price.  Two (and only two) entries out of (Price, Ratio, Denomination) must be provided.  So, to allow one entry out of the three to not be provided, we make all the three  nullable defaulting to zero and during validation we check if there is exactly one  of the three equal to zero.")
    price: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="The conversion price  Two (and only two) entries out of (Price, Ratio, Denomination) must be provided.  So, to allow one entry out of the three to not be provided, we make all the three  nullable defaulting to zero and during validation we check if there is exactly one  of the three equal to zero.")
    ratio: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="The number of common shares received at the time of conversion for each convertible bond  Two (and only two) entries out of (Price, Ratio, Denomination) must be provided.  So, to allow one entry out of the three to not be provided, we make all the three  nullable defaulting to zero and during validation we check if there is exactly one  of the three equal to zero.")
    __properties = ["date", "denomination", "price", "ratio"]

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
    def from_json(cls, json_str: str) -> BondConversionEntry:
        """Create an instance of BondConversionEntry from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BondConversionEntry:
        """Create an instance of BondConversionEntry from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BondConversionEntry.parse_obj(obj)

        _obj = BondConversionEntry.parse_obj({
            "var_date": obj.get("date"),
            "denomination": obj.get("denomination"),
            "price": obj.get("price"),
            "ratio": obj.get("ratio")
        })
        return _obj
