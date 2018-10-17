import typing
from generated_grpc import pipeline_pb2
from wrapper.pipeline.pipeline_description_output import PipelineDescriptionOutput


class PipelineOutputsFactory:

    @staticmethod
    def to_protobuf_outputs(outputs: typing.List[dict]) -> typing.List[pipeline_pb2.PipelineDescriptionOutput]:
        protobuf_pipeline_description_outputs = []
        for output in outputs:
            protobuf_pipeline_description_output = PipelineDescriptionOutput(output['name'], output['data']).to_protobuf()
            protobuf_pipeline_description_outputs.append(protobuf_pipeline_description_output)
        return protobuf_pipeline_description_outputs

    @staticmethod
    def from_protobuf_outputs(protobuf_outputs: typing.List[pipeline_pb2.PipelineDescriptionOutput]) -> typing.List[dict]:
        outputs: typing.List[dict] = []
        for protobuf_output in protobuf_outputs:
            output = {}
            output['name'] = protobuf_output.name
            output['data'] = protobuf_output.data
            outputs.append(output)
        return outputs

