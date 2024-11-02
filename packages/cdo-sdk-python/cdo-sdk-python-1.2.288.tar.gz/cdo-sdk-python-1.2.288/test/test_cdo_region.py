# coding: utf-8

"""
    Cisco Defense Orchestrator API

    Use the interactive documentation to explore the endpoints CDO has to offer

    The version of the OpenAPI document: 0.0.1
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from cdo_sdk_python.models.cdo_region import CdoRegion

class TestCdoRegion(unittest.TestCase):
    """CdoRegion unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CdoRegion:
        """Test CdoRegion
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CdoRegion`
        """
        model = CdoRegion()
        if include_optional:
            return CdoRegion(
                domain = '',
                api_domain = '',
                description = ''
            )
        else:
            return CdoRegion(
        )
        """

    def testCdoRegion(self):
        """Test CdoRegion"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
