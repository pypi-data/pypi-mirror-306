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
from lusid.models.comparison_attribute_value_pair import ComparisonAttributeValuePair

class GroupReconciliationCoreAttributeValues(BaseModel):
    """
    GroupReconciliationCoreAttributeValues
    """
    left_core_attributes: conlist(ComparisonAttributeValuePair) = Field(..., alias="leftCoreAttributes", description="Core attribute names and values for the left hand entity being reconciled.")
    right_core_attributes: conlist(ComparisonAttributeValuePair) = Field(..., alias="rightCoreAttributes", description="Core attribute names and values for the right hand entity being reconciled.")
    __properties = ["leftCoreAttributes", "rightCoreAttributes"]

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
    def from_json(cls, json_str: str) -> GroupReconciliationCoreAttributeValues:
        """Create an instance of GroupReconciliationCoreAttributeValues from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in left_core_attributes (list)
        _items = []
        if self.left_core_attributes:
            for _item in self.left_core_attributes:
                if _item:
                    _items.append(_item.to_dict())
            _dict['leftCoreAttributes'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in right_core_attributes (list)
        _items = []
        if self.right_core_attributes:
            for _item in self.right_core_attributes:
                if _item:
                    _items.append(_item.to_dict())
            _dict['rightCoreAttributes'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GroupReconciliationCoreAttributeValues:
        """Create an instance of GroupReconciliationCoreAttributeValues from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return GroupReconciliationCoreAttributeValues.parse_obj(obj)

        _obj = GroupReconciliationCoreAttributeValues.parse_obj({
            "left_core_attributes": [ComparisonAttributeValuePair.from_dict(_item) for _item in obj.get("leftCoreAttributes")] if obj.get("leftCoreAttributes") is not None else None,
            "right_core_attributes": [ComparisonAttributeValuePair.from_dict(_item) for _item in obj.get("rightCoreAttributes")] if obj.get("rightCoreAttributes") is not None else None
        })
        return _obj
