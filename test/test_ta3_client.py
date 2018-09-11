from __future__ import print_function

import grpc
import unittest
import pytest
from generated_grpc import core_pb2_grpc, core_pb2
import constants


class GrpcServerTestCase(unittest.TestCase):

    def setUp(self):
        self.protocol_version = core_pb2.DESCRIPTOR.GetOptions().Extensions[core_pb2.protocol_version]
        channel = grpc.insecure_channel('localhost:50052')
        self.stub = core_pb2_grpc.CoreStub(channel)

    # ------------------------------- Testing SearchSolutions ---------------------------------------------------------

    def test_search_solutions_error(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version='WRONG_VERSION')).result()
        expected_error_code = grpc.StatusCode.INVALID_ARGUMENT
        expected_error_message = constants.PROTOCOL_ERROR_MESSAGE

        assert cm.exception.code() == expected_error_code
        assert cm.exception.details() == expected_error_message

    def test_search_solutions_response(self):
        response = None
        try:
            response = self.stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=self.protocol_version))
        except Exception as e:
            pytest.fail(f'call to SearchSolutions failed to return a valid response with exception {str(e)}')

        assert isinstance(response, core_pb2.SearchSolutionsResponse), 'call to SearchSolutions did not return an instance of SearchSolutionsResponse' 

    def test_search_solutions_response_search_id(self):
        response_1 = self.stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=self.protocol_version))
        if not hasattr(response_1, 'search_id'):
            pytest.fail("SearchSolutionsResponse does not contain attribute 'search_id'")

        search_id_1 = response_1.search_id
        if len(search_id_1) < 22:
            pytest.fail(f'search_id %s returned in SearchSolutionsResponse is either empty or less than 22 characters {search_id_1}')

        response_2 = self.stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=self.protocol_version))
        search_id_2 = response_2.search_id
        assert search_id_1 != search_id_2, f'Two consecutive calls to SearchSolutions produced the same search_id: {search_id_1}'

    # ------------------------------- Testing GetSearchSolutionsResults -----------------------------------------------

    def test_get_search_solutions_results_error(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.GetSearchSolutionsResults(
                core_pb2.GetSearchSolutionsResultsRequest(search_id='WRONG_SEARCH_ID')).result()
        expected_error_code = grpc.StatusCode.INVALID_ARGUMENT
        expected_error_message = constants.SEARCH_ID_ERROR_MESSAGE
        assert cm.exception.code() == expected_error_code
        assert cm.exception.details() == expected_error_message

    def test_get_search_solutions_results_response(self):
        response = self.stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=self.protocol_version))
        search_id = response.search_id
        request = core_pb2.GetSearchSolutionsResultsRequest(search_id=search_id)
        try:
            for new_response in self.stub.GetSearchSolutionsResults(request):
                if not hasattr(new_response, 'progress'):
                    pytest.fail('GetSearchSolutionsResultsResponse does not contain attribute \'progress\'')
        except Exception as e:
            pytest.fail(f'call to GetSearchSolutionsResults failed to return a valid response stream with exception {str(e)}')

    def test_end_search_solutions_error(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.EndSearchSolutions(core_pb2.EndSearchSolutionsRequest(search_id='WRONG_SEARCH_ID'))
        expected_error_code = grpc.StatusCode.INVALID_ARGUMENT
        expected_error_message = 'search_id argument provided in EndSearchSolutionsRequest does not match any search_process'
        assert cm.exception.code() == expected_error_code
        assert cm.exception.details() == expected_error_message

    # ------------------------------- Testing StopSearchSolutions -----------------------------------------------------

    def test_stop_search_solutions_error(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.StopSearchSolutions(core_pb2.StopSearchSolutionsRequest(search_id='WRONG_SEARCH_ID'))
        expected_error_code = grpc.StatusCode.INVALID_ARGUMENT
        expected_error_message = 'search_id argument provided in StopSearchSolutionsRequest does not match any search_process'
        assert cm.exception.code() == expected_error_code
        assert cm.exception.details() == expected_error_message

    # ------------------------------- Testing DescribeSolution --------------------------------------------------------

    def test_describe_solution_error(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.DescribeSolution(core_pb2.DescribeSolutionRequest(solution_id='WRONG_SOLUTION_ID'))
        expected_error_code = grpc.StatusCode.INVALID_ARGUMENT
        expected_error_message = 'solution_id argument provided in DescribeSolutionRequest does not match any solution_id'
        assert cm.exception.code() == expected_error_code
        assert cm.exception.details() == expected_error_message

    # ------------------------------- Testing DescribeSolution --------------------------------------------------------

    def test_score_solution_error(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.ScoreSolution(core_pb2.ScoreSolutionRequest(solution_id='WRONG_SOLUTION_ID'))
        expected_error_code = grpc.StatusCode.INVALID_ARGUMENT
        expected_error_message = 'solution_id argument provided in ScoreSolutionRequest does not match any solution_id'
        assert cm.exception.code() == expected_error_code
        assert cm.exception.details() == expected_error_message
