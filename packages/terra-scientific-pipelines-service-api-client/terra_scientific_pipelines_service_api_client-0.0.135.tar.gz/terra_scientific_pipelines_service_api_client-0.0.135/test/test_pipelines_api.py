# coding: utf-8

"""
    Terra Scientific Pipelines Service

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from teaspoons_client.api.pipelines_api import PipelinesApi


class TestPipelinesApi(unittest.TestCase):
    """PipelinesApi unit test stubs"""

    def setUp(self) -> None:
        self.api = PipelinesApi()

    def tearDown(self) -> None:
        pass

    def test_get_pipeline_details(self) -> None:
        """Test case for get_pipeline_details

        Return info about the specified pipeline
        """
        pass

    def test_get_pipelines(self) -> None:
        """Test case for get_pipelines

        Return all available Pipelines
        """
        pass


if __name__ == '__main__':
    unittest.main()
