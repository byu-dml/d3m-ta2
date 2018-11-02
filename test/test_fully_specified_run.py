import pytest
from generated_grpc import core_pb2, core_pb2_grpc, pipeline_pb2
from d3m.metadata import pipeline as pipeline_module
from factory.pipeline_description_factory import PipelineDescriptionFactory
import generated_grpc.problem_pb2 as grpc_problem


class TestFullySpecifiedRun:

    @staticmethod
    def test_fully_specified_pipelines(stub: core_pb2_grpc.CoreStub, protocol_version: str, random_forest_pipeline_fully_specified: pipeline_module.Pipeline, sick_problem: grpc_problem.ProblemDescription):
        pipeline_description: pipeline_pb2.PipelineDescription = PipelineDescriptionFactory.to_protobuf_pipeline_description(random_forest_pipeline_fully_specified)
        request = core_pb2.SearchSolutionsRequest(version=protocol_version,
                                                  template=pipeline_description,
                                                  problem=sick_problem
                                                  )
        response: core_pb2.DescribeSolutionResponse = stub.SearchSolutions(request)
        search_id = response.search_id
        request = core_pb2.GetSearchSolutionsResultsRequest(search_id=search_id)
        test = stub.GetSearchSolutionsResults(request)
        for result in test:
            assert hasattr(result, 'progress'), 'GetSearchSolutionsResultsResponse does not contain attribute \'progress\''
            progress: core_pb2.Progress = result.progress
            completed = 3
            assert progress.state == completed, 'Search should be done for a fully specified pipeline'
            assert hasattr(result, 'done_ticks'), 'GetSearchSolutionsResultsResponse does not contain attribute \'done_ticks\''
            assert hasattr(result, 'all_ticks'), 'GetSearchSolutionsResultsResponse does not contain attribute \'all_ticks\''
            assert hasattr(result, 'solution_id'), 'GetSearchSolutionsResultsResponse does not contain attribute \'solution_id\''
            assert isinstance(result, core_pb2.GetSearchSolutionsResultsResponse), 'GetSearchSolutionsResponse not returned'

        assert isinstance(response, core_pb2.SearchSolutionsResponse), 'call to SearchSolutions with fully specified pipeline did not return an instance of SearchSolutionsResponse'


    @staticmethod
    def test_fully_specified_pipeline_run(solution_id_fully_specified):
        # assert False
        assert isinstance(solution_id_fully_specified, str)
