# coding: utf-8

"""
    Terra Scientific Pipelines Service

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from teaspoons_client.models.get_jobs_response import GetJobsResponse

class TestGetJobsResponse(unittest.TestCase):
    """GetJobsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetJobsResponse:
        """Test GetJobsResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetJobsResponse`
        """
        model = GetJobsResponse()
        if include_optional:
            return GetJobsResponse(
                total_results = 56,
                page_token = '',
                results = [
                    teaspoons_client.models.job_report.JobReport(
                        id = '', 
                        description = '', 
                        status = 'RUNNING', 
                        status_code = 56, 
                        submitted = '', 
                        completed = '', 
                        result_url = '', )
                    ]
            )
        else:
            return GetJobsResponse(
        )
        """

    def testGetJobsResponse(self):
        """Test GetJobsResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
