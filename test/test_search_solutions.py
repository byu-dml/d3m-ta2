import pytest
import generated_grpc.problem_pb2 as grpc_problem
from generated_grpc import core_pb2, core_pb2_grpc, pipeline_pb2
from d3m.metadata import pipeline as pipeline_module
from wrapper.pipeline_description import PipelineDescription


class TestSearchSolutions:

    @staticmethod
    def test_search_solutions_response_1(stub: core_pb2_grpc.CoreStub, protocol_version: str, sick_problem: grpc_problem.ProblemDescription):
        response = None
        try:
            response = stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=protocol_version, problem=sick_problem))
        except Exception as e:
            pytest.fail(f'call to SearchSolutions failed to return a valid response with exception {str(e)}')

        assert isinstance(response, core_pb2.SearchSolutionsResponse), 'call to SearchSolutions did not return an instance of SearchSolutionsResponse'

    @staticmethod
    def test_search_solutions_response_search_id(stub: core_pb2_grpc.CoreStub, protocol_version: str, sick_problem: grpc_problem.ProblemDescription):
        response_1 = stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=protocol_version, problem=sick_problem))
        if not hasattr(response_1, 'search_id'):
            pytest.fail("SearchSolutionsResponse does not contain attribute 'search_id'")

        search_id_1 = response_1.search_id
        if len(search_id_1) < 22:
            pytest.fail(f'search_id %s returned in SearchSolutionsResponse is either empty or less than 22 characters {search_id_1}')

        response_2 = stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=protocol_version, problem=sick_problem))
        search_id_2 = response_2.search_id
        assert search_id_1 != search_id_2, f'Two consecutive calls to SearchSolutions produced the same search_id: {search_id_1}'

    @staticmethod
    def test_get_search_solutions_results_response(stub: core_pb2_grpc.CoreStub, protocol_version: str, sick_problem: grpc_problem.ProblemDescription):
        solutions_request = core_pb2.SearchSolutionsRequest(version=protocol_version, problem=sick_problem)
        response = stub.SearchSolutions(solutions_request)
        search_id = response.search_id
        get_search_solutions_request = core_pb2.GetSearchSolutionsResultsRequest(search_id=search_id)
        received_result = False
        try:
            results = stub.GetSearchSolutionsResults(get_search_solutions_request)
            for new_response in results:
                received_result = True
                assert hasattr(new_response, 'progress'), 'GetSearchSolutionsResultsResponse does not contain attribute \'progress\''
                assert hasattr(new_response, 'done_ticks'), 'GetSearchSolutionsResultsResponse does not contain attribute \'done_ticks\''
                assert hasattr(new_response, 'all_ticks'), 'GetSearchSolutionsResultsResponse does not contain attribute \'all_ticks\''
                assert hasattr(new_response, 'solution_id'), 'GetSearchSolutionsResultsResponse does not contain attribute \'solution_id\''
                assert isinstance(new_response, core_pb2.GetSearchSolutionsResultsResponse), 'GetSearchSolutionsResponse not returned'

        except Exception as e:
            pytest.fail(f'call to GetSearchSolutionsResults failed to return a valid response stream with exception {str(e)}')
        assert received_result, 'No search results received'

    @staticmethod
    def test_fully_specified_pipelines(stub: core_pb2_grpc.CoreStub, protocol_version: str, random_forest_pipeline: pipeline_module.Pipeline, sick_problem: grpc_problem.ProblemDescription):
        pipeline_description: pipeline_pb2.PipelineDescription = PipelineDescription.pipeline_to_protobuf_pipeline(random_forest_pipeline)
        request = core_pb2.SearchSolutionsRequest(version=protocol_version,
                                                  template=pipeline_description,
                                                  problem=sick_problem
                                                  )
        response = stub.SearchSolutions(request)
        assert False
        assert isinstance(response, core_pb2.SearchSolutionsResponse), 'call to SearchSolutions with fully specified pipeline did not return an instance of SearchSolutionsResponse'

    @staticmethod
    def test_start_search_of_short_time_bound(stub: core_pb2_grpc.CoreStub, protocol_version: str, sick_problem: grpc_problem.ProblemDescription):
        solutions_request = core_pb2.SearchSolutionsRequest(version=protocol_version,
                                                            problem=sick_problem,
                                                            time_bound=.00001
                                                            )
        response = stub.SearchSolutions(solutions_request)
        search_id = response.search_id
        get_search_solutions_request = core_pb2.GetSearchSolutionsResultsRequest(search_id=search_id)
        try:
            results = stub.GetSearchSolutionsResults(get_search_solutions_request)
            for new_response in results:
                pytest.fail('Search should have been stopped before any results were retrieved')

        except Exception as e:
            pytest.fail(f'call to GetSearchSolutionsResults failed to return a valid response stream with exception {str(e)}')



