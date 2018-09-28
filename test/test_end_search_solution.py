from generated_grpc import core_pb2, core_pb2_grpc
import pytest
import grpc


class TestEndSearchSolution:

    @staticmethod
    def test_end_search_solution_correct_response(search_id: str, stub: core_pb2_grpc.CoreStub):
        request = core_pb2.EndSearchSolutionsRequest(search_id=search_id)
        response = stub.EndSearchSolutions(request)
        assert response is not None
        assert isinstance(response, core_pb2.EndSearchSolutionsResponse), 'EndSearchSolutionsResponse not returned'

    @staticmethod
    def test_end_search_solution_removed_search(search_id: str, stub: core_pb2_grpc.CoreStub):
        end_solutions_request = core_pb2.EndSearchSolutionsRequest(search_id=search_id)
        stub.EndSearchSolutions(end_solutions_request)
        with pytest.raises(grpc.RpcError):
            get_search_solutions_request = core_pb2.GetSearchSolutionsResultsRequest(search_id=search_id)
            stub.GetSearchSolutionsResults(get_search_solutions_request).result()


