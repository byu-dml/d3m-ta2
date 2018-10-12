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

