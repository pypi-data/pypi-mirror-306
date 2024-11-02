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


from typing import Any, Dict, List
from pydantic.v1 import BaseModel, Field, conlist
from lusid.models.amortisation_rule import AmortisationRule
from lusid.models.date_range import DateRange

class RulesInterval(BaseModel):
    """
    RulesInterval
    """
    effective_range: DateRange = Field(..., alias="effectiveRange")
    rules: conlist(AmortisationRule, max_items=100) = Field(..., description="The rules of this rule set.")
    __properties = ["effectiveRange", "rules"]

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
    def from_json(cls, json_str: str) -> RulesInterval:
        """Create an instance of RulesInterval from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of effective_range
        if self.effective_range:
            _dict['effectiveRange'] = self.effective_range.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in rules (list)
        _items = []
        if self.rules:
            for _item in self.rules:
                if _item:
                    _items.append(_item.to_dict())
            _dict['rules'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RulesInterval:
        """Create an instance of RulesInterval from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RulesInterval.parse_obj(obj)

        _obj = RulesInterval.parse_obj({
            "effective_range": DateRange.from_dict(obj.get("effectiveRange")) if obj.get("effectiveRange") is not None else None,
            "rules": [AmortisationRule.from_dict(_item) for _item in obj.get("rules")] if obj.get("rules") is not None else None
        })
        return _obj
