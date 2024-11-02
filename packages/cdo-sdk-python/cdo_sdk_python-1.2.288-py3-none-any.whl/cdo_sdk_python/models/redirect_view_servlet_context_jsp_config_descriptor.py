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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from cdo_sdk_python.models.redirect_view_servlet_context_jsp_config_descriptor_jsp_property_groups_inner import RedirectViewServletContextJspConfigDescriptorJspPropertyGroupsInner
from cdo_sdk_python.models.redirect_view_servlet_context_jsp_config_descriptor_taglibs_inner import RedirectViewServletContextJspConfigDescriptorTaglibsInner
from typing import Optional, Set
from typing_extensions import Self

class RedirectViewServletContextJspConfigDescriptor(BaseModel):
    """
    RedirectViewServletContextJspConfigDescriptor
    """ # noqa: E501
    jsp_property_groups: Optional[List[RedirectViewServletContextJspConfigDescriptorJspPropertyGroupsInner]] = Field(default=None, alias="jspPropertyGroups")
    taglibs: Optional[List[RedirectViewServletContextJspConfigDescriptorTaglibsInner]] = None
    __properties: ClassVar[List[str]] = ["jspPropertyGroups", "taglibs"]

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
        """Create an instance of RedirectViewServletContextJspConfigDescriptor from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in jsp_property_groups (list)
        _items = []
        if self.jsp_property_groups:
            for _item in self.jsp_property_groups:
                if _item:
                    _items.append(_item.to_dict())
            _dict['jspPropertyGroups'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in taglibs (list)
        _items = []
        if self.taglibs:
            for _item in self.taglibs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['taglibs'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RedirectViewServletContextJspConfigDescriptor from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "jspPropertyGroups": [RedirectViewServletContextJspConfigDescriptorJspPropertyGroupsInner.from_dict(_item) for _item in obj["jspPropertyGroups"]] if obj.get("jspPropertyGroups") is not None else None,
            "taglibs": [RedirectViewServletContextJspConfigDescriptorTaglibsInner.from_dict(_item) for _item in obj["taglibs"]] if obj.get("taglibs") is not None else None
        })
        return _obj


