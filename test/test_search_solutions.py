import pytest
from generated_grpc import core_pb2, core_pb2_grpc, pipeline_pb2, primitive_pb2
from d3m.metadata import pipeline as pipeline_module
import d3m.container as container
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

        pipeline_inputs: typing.List[dict] = TestSearchSolutions.get_pipeline_inputs(pipeline)
        pipeline_outputs = TestSearchSolutions.get_pipeline_outputs(pipeline)
        pipeline_steps: typing.List[pipeline_pb2.PipelineDescriptionStep] = TestSearchSolutions.get_pipeline_steps(pipeline)
        created = TestSearchSolutions.get_protobuf_timestamp(pipeline)

        pipeline_name = pipeline.name
        pipeline_description = pipeline.description

        return pipeline_pb2.PipelineDescription(created=created,
                                                name=pipeline_name,
                                                description=pipeline_description,
                                                inputs=pipeline_inputs,
                                                outputs=pipeline_outputs,
                                                steps=pipeline_steps
                                                )

    @staticmethod
    def get_pipeline_outputs(pipeline: pipeline_module.Pipeline) -> typing.List[pipeline_pb2.PipelineDescriptionOutput]:
        outputs = []
        for output in pipeline.outputs:
            description_output = pipeline_pb2.PipelineDescriptionOutput(name=output['name'], data=output['data'])
            outputs.append(description_output)
        return outputs

    @staticmethod
    def get_pipeline_inputs(pipeline: pipeline_module.Pipeline) -> typing.List[pipeline_pb2.PipelineDescriptionInput]:
        pipeline_description_inputs = []
        for input_ in pipeline.inputs:
            input_name = input_['name']
            description_input = pipeline_pb2.PipelineDescriptionInput(name=input_name)
            pipeline_description_inputs.append(description_input)

        return pipeline_description_inputs

    @staticmethod
    def get_pipeline_steps(pipeline: pipeline_module.Pipeline) -> typing.List[pipeline_pb2.PipelineDescriptionStep]:
        steps = []
        for step in pipeline.steps:
            if isinstance(step, pipeline_module.PrimitiveStep):
                primitive_description = step.primitive_description
                primitive = TestSearchSolutions.get_primitive_from_description(primitive_description)
                arguments = step.arguments
                primitive_step_arguments = TestSearchSolutions.get_primitive_step_arguments(arguments)

                primitive_description_step = pipeline_pb2.PrimitivePipelineDescriptionStep(primitive=primitive,
                                                                                           arguments=primitive_step_arguments)

                pipeline_description_step = pipeline_pb2.PipelineDescriptionStep(primitive=primitive_description_step)
                steps.append(pipeline_description_step)
        return steps

    @staticmethod
    def get_primitive_step_arguments(arguments: dict) -> typing.Dict[str, pipeline_pb2.PrimitiveStepArgument]:
        primitive_step_arguments = {}
        for key, argument in arguments.items():
            data = argument['data']
            type_ = argument['type']

            primitive_step_argument = None
            if type_ == pipeline_module.ArgumentType.CONTAINER:
                container_argument = pipeline_pb2.ContainerArgument(data=data)
                primitive_step_argument = pipeline_pb2.PrimitiveStepArgument(container=container_argument)
            elif type_ == pipeline_module.ArgumentType.DATA:
                data_argument = pipeline_pb2.DataArgument(date=data)
                primitive_step_argument = pipeline_pb2.PrimitiveStepArgument(data=data_argument)
            else:
                pytest.fail(f"Invalid type for argument {argument}")

            primitive_step_arguments[key] = primitive_step_argument

        return primitive_step_arguments

    @staticmethod
    def get_primitive_from_description(primitive_description: dict) -> pipeline_pb2.primitive__pb2.Primitive:
        id_ = primitive_description['id']
        version = primitive_description['version']
        python_path = primitive_description['python_path']
        name = primitive_description['name']
        digest = None
        if 'digest' in primitive_description:
            digest = primitive_description['digest']

        primitive = pipeline_pb2.primitive__pb2.Primitive(id=id_, version=version, python_path=python_path, name=name, digest=digest)
        return primitive

    @staticmethod
    def get_protobuf_timestamp(pipeline: pipeline_module.Pipeline) -> Timestamp:
        created_datetime: datetime.datetime = pipeline.created
        created_datetime = created_datetime.replace(tzinfo=None)
        created: Timestamp = Timestamp()
        created.FromDatetime(created_datetime)
        return created


