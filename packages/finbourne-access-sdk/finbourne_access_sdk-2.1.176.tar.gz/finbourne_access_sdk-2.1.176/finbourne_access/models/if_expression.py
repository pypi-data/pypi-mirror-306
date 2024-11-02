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


from typing import Any, Dict, Optional
from pydantic.v1 import BaseModel, Field
from finbourne_access.models.if_feature_chain_expression import IfFeatureChainExpression
from finbourne_access.models.if_identity_claim_expression import IfIdentityClaimExpression
from finbourne_access.models.if_identity_scope_expression import IfIdentityScopeExpression
from finbourne_access.models.if_request_header_expression import IfRequestHeaderExpression

class IfExpression(BaseModel):
    """
    IfExpression
    """
    if_request_header_expression: Optional[IfRequestHeaderExpression] = Field(None, alias="ifRequestHeaderExpression")
    if_identity_claim_expression: Optional[IfIdentityClaimExpression] = Field(None, alias="ifIdentityClaimExpression")
    if_identity_scope_expression: Optional[IfIdentityScopeExpression] = Field(None, alias="ifIdentityScopeExpression")
    if_feature_chain_expression: Optional[IfFeatureChainExpression] = Field(None, alias="ifFeatureChainExpression")
    __properties = ["ifRequestHeaderExpression", "ifIdentityClaimExpression", "ifIdentityScopeExpression", "ifFeatureChainExpression"]

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
    def from_json(cls, json_str: str) -> IfExpression:
        """Create an instance of IfExpression from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of if_request_header_expression
        if self.if_request_header_expression:
            _dict['ifRequestHeaderExpression'] = self.if_request_header_expression.to_dict()
        # override the default output from pydantic by calling `to_dict()` of if_identity_claim_expression
        if self.if_identity_claim_expression:
            _dict['ifIdentityClaimExpression'] = self.if_identity_claim_expression.to_dict()
        # override the default output from pydantic by calling `to_dict()` of if_identity_scope_expression
        if self.if_identity_scope_expression:
            _dict['ifIdentityScopeExpression'] = self.if_identity_scope_expression.to_dict()
        # override the default output from pydantic by calling `to_dict()` of if_feature_chain_expression
        if self.if_feature_chain_expression:
            _dict['ifFeatureChainExpression'] = self.if_feature_chain_expression.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IfExpression:
        """Create an instance of IfExpression from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IfExpression.parse_obj(obj)

        _obj = IfExpression.parse_obj({
            "if_request_header_expression": IfRequestHeaderExpression.from_dict(obj.get("ifRequestHeaderExpression")) if obj.get("ifRequestHeaderExpression") is not None else None,
            "if_identity_claim_expression": IfIdentityClaimExpression.from_dict(obj.get("ifIdentityClaimExpression")) if obj.get("ifIdentityClaimExpression") is not None else None,
            "if_identity_scope_expression": IfIdentityScopeExpression.from_dict(obj.get("ifIdentityScopeExpression")) if obj.get("ifIdentityScopeExpression") is not None else None,
            "if_feature_chain_expression": IfFeatureChainExpression.from_dict(obj.get("ifFeatureChainExpression")) if obj.get("ifFeatureChainExpression") is not None else None
        })
        return _obj
