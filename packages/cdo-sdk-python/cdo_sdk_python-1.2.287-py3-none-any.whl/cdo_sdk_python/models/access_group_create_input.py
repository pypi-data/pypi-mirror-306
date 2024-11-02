# coding: utf-8

"""
    CDO API

    Use the documentation to explore the endpoints CDO has to offer

    The version of the OpenAPI document: 1.5.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class AccessGroupCreateInput(BaseModel):
    """
    AccessGroupCreateInput
    """ # noqa: E501
    name: Optional[StrictStr] = Field(default=None, description="A human-readable name for the Access Group.")
    entity_uid: StrictStr = Field(description="The unique identifier, represented as a UUID, of the device/manager associated with the Access Group. When creating shared Access Group, entityUid represents device that contains source Access Group ", alias="entityUid")
    resources: Optional[List[Dict[str, Dict[str, Any]]]] = Field(default=None, description="The set of of interface and direction pairs or global resource.  Resource is an attribute applicable only to devices and will not be propagated to appliedTo devices if Access Group is shared.")
    is_shared: Optional[StrictBool] = Field(default=None, description="The flag that identifies if access group is shared.  If set to true, appliedTo field should be provided as well and entityUid should point to source device.", alias="isShared")
    applied_to: Optional[List[StrictStr]] = Field(default=None, description="The set of device unique identifiers to which this Access Group was applied. Only valid for shared access group.", alias="appliedTo")
    __properties: ClassVar[List[str]] = ["name", "entityUid", "resources", "isShared", "appliedTo"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of AccessGroupCreateInput from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AccessGroupCreateInput from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "entityUid": obj.get("entityUid"),
            "resources": obj.get("resources"),
            "isShared": obj.get("isShared"),
            "appliedTo": obj.get("appliedTo")
        })
        return _obj


