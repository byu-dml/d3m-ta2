import typing
from generated_grpc import pipeline_pb2
from wrapper.pipeline.pipeline_description_input import PipelineDescriptionInput


class PipelineInputsFactory:

    @staticmethod
    def to_protobuf_inputs(inputs: typing.List[dict]) -> typing.List[pipeline_pb2.PipelineDescriptionInput]:
        protobuf_pipeline_description_inputs = []
        for input_ in inputs:
            protobuf_pipeline_description_input = PipelineDescriptionInput(input_['name']).to_protobuf()
            protobuf_pipeline_description_inputs.append(protobuf_pipeline_description_input)
        return protobuf_pipeline_description_inputs

    @staticmethod
    def from_protobuf_inputs(protobuf_inputs: typing.List[pipeline_pb2.PipelineDescriptionInput]) -> typing.List[str]:
        pipeline_inputs = []
        for protobuf_input in protobuf_inputs:
            pipeline_inputs.append(protobuf_input.name)
        return pipeline_inputs
