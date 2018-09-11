from __future__ import print_function

import grpc
import unittest
import pytest
from generated_grpc import core_pb2_grpc, core_pb2
import constants


class TestIncorrectParams(unittest.TestCase):

    def setUp(self):
        self.protocol_version = core_pb2.DESCRIPTOR.GetOptions().Extensions[core_pb2.protocol_version]
        channel = grpc.insecure_channel('localhost:50052')
        self.stub = core_pb2_grpc.CoreStub(channel)

    def test_search_solutions_error(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version='WRONG_VERSION')).result()
        expected_error_code = grpc.StatusCode.INVALID_ARGUMENT
        expected_error_message = constants.PROTOCOL_ERROR_MESSAGE

        assert cm.exception.code() == expected_error_code
        assert cm.exception.details() == expected_error_message

    def test_get_search_solutions_results_error(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.GetSearchSolutionsResults(
                core_pb2.GetSearchSolutionsResultsRequest(search_id='WRONG_SEARCH_ID')).result()
        expected_error_code = grpc.StatusCode.INVALID_ARGUMENT
        expected_error_message = constants.SEARCH_ID_ERROR_MESSAGE
        assert cm.exception.code() == expected_error_code
        assert cm.exception.details() == expected_error_message

    def test_end_search_solutions_error(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.EndSearchSolutions(core_pb2.EndSearchSolutionsRequest(search_id='WRONG_SEARCH_ID'))
        expected_error_code = grpc.StatusCode.INVALID_ARGUMENT
        expected_error_message = constants.END_SEARCH_SOLUTIONS_ERROR_MESSAGE
        assert cm.exception.code() == expected_error_code
        assert cm.exception.details() == expected_error_message

    def test_stop_search_solutions_error(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.StopSearchSolutions(core_pb2.StopSearchSolutionsRequest(search_id='WRONG_SEARCH_ID'))
        expected_error_code = grpc.StatusCode.INVALID_ARGUMENT
        expected_error_message = constants.STOP_SEARCH_SOLUTIONS_ERROR_MESSAGE
        assert cm.exception.code() == expected_error_code
        assert cm.exception.details() == expected_error_message

    def test_describe_solution_error(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.DescribeSolution(core_pb2.DescribeSolutionRequest(solution_id='WRONG_SOLUTION_ID'))
        expected_error_code = grpc.StatusCode.INVALID_ARGUMENT
        expected_error_message = constants.DESCRIBE_SOLUTION_ERROR_MESSAGE
        assert cm.exception.code() == expected_error_code
        assert cm.exception.details() == expected_error_message

    def test_score_solution_error(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.ScoreSolution(core_pb2.ScoreSolutionRequest(solution_id='WRONG_SOLUTION_ID'))
        expected_error_code = grpc.StatusCode.INVALID_ARGUMENT
        expected_error_message = constants.SCORE_SOLUTION_ERROR_MESSAGE
        assert cm.exception.code() == expected_error_code
        assert cm.exception.details() == expected_error_message
