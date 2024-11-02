# coding: utf-8

"""
    FINBOURNE Access Management API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict, List, Optional
from pydantic.v1 import BaseModel, Field, StrictStr, conlist, constr
from finbourne_access.models.action_id import ActionId

class IdSelectorDefinition(BaseModel):
    """
    IdSelectorDefinition
    """
    identifier: Dict[str, StrictStr] = Field(...)
    actions: conlist(ActionId, min_items=1) = Field(...)
    name: Optional[constr(strict=True, max_length=100, min_length=0)] = None
    description: Optional[constr(strict=True, max_length=1024, min_length=0)] = None
    __properties = ["identifier", "actions", "name", "description"]

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
    def from_json(cls, json_str: str) -> IdSelectorDefinition:
        """Create an instance of IdSelectorDefinition from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in actions (list)
        _items = []
        if self.actions:
            for _item in self.actions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['actions'] = _items
        # set to None if name (nullable) is None
        # and __fields_set__ contains the field
        if self.name is None and "name" in self.__fields_set__:
            _dict['name'] = None

        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IdSelectorDefinition:
        """Create an instance of IdSelectorDefinition from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IdSelectorDefinition.parse_obj(obj)

        _obj = IdSelectorDefinition.parse_obj({
            "identifier": obj.get("identifier"),
            "actions": [ActionId.from_dict(_item) for _item in obj.get("actions")] if obj.get("actions") is not None else None,
            "name": obj.get("name"),
            "description": obj.get("description")
        })
        return _obj
