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


from typing import Any, Dict, List
from pydantic.v1 import BaseModel, Field, conlist
from finbourne_access.models.policy_id import PolicyId

class AddPolicyToRoleRequest(BaseModel):
    """
    Request body used to add Policies to a Role  # noqa: E501
    """
    policies: conlist(PolicyId) = Field(..., description="Identifiers of policies to add to a role")
    __properties = ["policies"]

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
    def from_json(cls, json_str: str) -> AddPolicyToRoleRequest:
        """Create an instance of AddPolicyToRoleRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in policies (list)
        _items = []
        if self.policies:
            for _item in self.policies:
                if _item:
                    _items.append(_item.to_dict())
            _dict['policies'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddPolicyToRoleRequest:
        """Create an instance of AddPolicyToRoleRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AddPolicyToRoleRequest.parse_obj(obj)

        _obj = AddPolicyToRoleRequest.parse_obj({
            "policies": [PolicyId.from_dict(_item) for _item in obj.get("policies")] if obj.get("policies") is not None else None
        })
        return _obj
