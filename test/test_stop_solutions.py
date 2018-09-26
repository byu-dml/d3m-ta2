from generated_grpc import core_pb2_grpc, core_pb2


class TestStopSolutions:

    @staticmethod
    def test_stop_solutions_successful(search_id: str, stub: core_pb2_grpc.CoreStub):
        request = core_pb2.StopSearchSolutionsRequest(search_id=search_id)
        response: core_pb2.StopSearchSolutionsResponse = stub.StopSearchSolutions(request)
        assert isinstance(response, core_pb2.StopSearchSolutionsResponse), 'StopSearchSolutionsResponse not returned'

