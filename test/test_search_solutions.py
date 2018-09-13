import pytest
from generated_grpc import core_pb2, core_pb2_grpc, pipeline_pb2, primitive_pb2
from d3m.metadata import pipeline as pipeline_module
from pprint import pprint
import typing
import datetime
from google.protobuf.timestamp_pb2 import Timestamp


class TestSearchSolutions:

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

    @staticmethod
    def test_fully_specified_pipelines(stub: core_pb2_grpc.CoreStub, protocol_version: str, random_forest_pipeline: pipeline_module.Pipeline):
        pipeline_description: pipeline_pb2.PipelineDescription = TestSearchSolutions.python_pipeline_to_protocol_pipeline(random_forest_pipeline)
        # pprint(pipeline_description)
        assert False
        # pipeline_description.

    @staticmethod
    def python_pipeline_to_protocol_pipeline(pipeline: pipeline_module.Pipeline) -> pipeline_pb2.PipelineDescription:
        created_datetime: datetime.datetime = pipeline.created
        created = TestSearchSolutions.get_protobuf_timestamp(created_datetime)
        name = pipeline.name
        description = pipeline.description
        inputs: typing.List[dict] = []
        for input in pipeline.inputs:
            input_name = input['name']
            description_input = pipeline_pb2.PipelineDescriptionInput(name=input_name)
            inputs.append(description_input)
        outputs = []
        for output in pipeline.outputs:
            description_output = pipeline_pb2.PipelineDescriptionOutput(name=output['name'], data=output['data'])
            outputs.append(description_output)

        # pprint(pipeline.steps)
        steps: typing.List[pipeline_pb2.PipelineDescriptionStep] = []
        for step in pipeline.steps:
            if isinstance(step, pipeline_module.PrimitiveStep):
                pprint(dir(step.primitive))
                description_step = pipeline_pb2.PipelineDescriptionStep()
                description_step.step = pipeline_pb2.PrimitivePipelineDescriptionStep()
                steps.append(step)

        pprint(steps)
        return pipeline_pb2.PipelineDescription(created=created, name=name, description=description, inputs=inputs, outputs=outputs, steps=steps)
        # assuming each step is a primitive for now, this should be changed
        #for step in python_pipeline.steps:

    @staticmethod
    def get_protobuf_timestamp(created_datetime):
        created_datetime = created_datetime.replace(tzinfo=None)
        created: Timestamp = Timestamp()
        created.FromDatetime(created_datetime)
        return created


