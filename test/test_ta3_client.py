from __future__ import print_function

import pytest
from generated_grpc import core_pb2, core_pb2_grpc


class TestTa3Client:

    @staticmethod
    def test_search_solutions_response(stub: core_pb2_grpc.CoreStub, protocol_version: str):
        response = None
        try:
            response = stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=protocol_version))
        except Exception as e:
            pytest.fail(f'call to SearchSolutions failed to return a valid response with exception {str(e)}')

        assert isinstance(response, core_pb2.SearchSolutionsResponse), 'call to SearchSolutions did not return an instance of SearchSolutionsResponse' 

    @staticmethod
    def test_search_solutions_response_search_id(stub: core_pb2_grpc.CoreStub, protocol_version: str):
        response_1 = stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=protocol_version))
        if not hasattr(response_1, 'search_id'):
            pytest.fail("SearchSolutionsResponse does not contain attribute 'search_id'")

        search_id_1 = response_1.search_id
        if len(search_id_1) < 22:
            pytest.fail(f'search_id %s returned in SearchSolutionsResponse is either empty or less than 22 characters {search_id_1}')

        response_2 = stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=protocol_version))
        search_id_2 = response_2.search_id
        assert search_id_1 != search_id_2, f'Two consecutive calls to SearchSolutions produced the same search_id: {search_id_1}'

    @staticmethod
    def test_get_search_solutions_results_response(stub: core_pb2_grpc.CoreStub, protocol_version: str):
        response = stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=protocol_version))
        search_id = response.search_id
        request = core_pb2.GetSearchSolutionsResultsRequest(search_id=search_id)
        try:
            for new_response in stub.GetSearchSolutionsResults(request):
                if not hasattr(new_response, 'progress'):
                    pytest.fail('GetSearchSolutionsResultsResponse does not contain attribute \'progress\'')
        except Exception as e:
            pytest.fail(f'call to GetSearchSolutionsResults failed to return a valid response stream with exception {str(e)}')

