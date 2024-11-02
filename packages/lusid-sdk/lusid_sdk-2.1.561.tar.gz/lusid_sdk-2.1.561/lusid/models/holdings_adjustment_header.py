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
from typing import Any, Dict, List, Optional
from pydantic.v1 import BaseModel, Field, StrictStr, conlist, validator
from lusid.models.link import Link
from lusid.models.version import Version

class HoldingsAdjustmentHeader(BaseModel):
    """
    A record of holdings adjustments made on the transaction portfolio.  # noqa: E501
    """
    effective_at: datetime = Field(..., alias="effectiveAt", description="The effective datetime from which the adjustment is valid. There can only be one holdings adjustment for a transaction portfolio at a specific effective datetime, so this uniquely identifies the adjustment.")
    version: Version = Field(...)
    unmatched_holding_method: StrictStr = Field(..., alias="unmatchedHoldingMethod", description="Describes how the holdings were adjusted. If 'PositionToZero' the entire transaction portfolio's holdings were set via a call to 'Set holdings'. If 'KeepTheSame' only the specified holdings were adjusted via a call to 'Adjust holdings'. The available values are: PositionToZero, KeepTheSame")
    links: Optional[conlist(Link)] = None
    __properties = ["effectiveAt", "version", "unmatchedHoldingMethod", "links"]

    @validator('unmatched_holding_method')
    def unmatched_holding_method_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('PositionToZero', 'KeepTheSame'):
            raise ValueError("must be one of enum values ('PositionToZero', 'KeepTheSame')")
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
    def from_json(cls, json_str: str) -> HoldingsAdjustmentHeader:
        """Create an instance of HoldingsAdjustmentHeader from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of version
        if self.version:
            _dict['version'] = self.version.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> HoldingsAdjustmentHeader:
        """Create an instance of HoldingsAdjustmentHeader from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return HoldingsAdjustmentHeader.parse_obj(obj)

        _obj = HoldingsAdjustmentHeader.parse_obj({
            "effective_at": obj.get("effectiveAt"),
            "version": Version.from_dict(obj.get("version")) if obj.get("version") is not None else None,
            "unmatched_holding_method": obj.get("unmatchedHoldingMethod"),
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
