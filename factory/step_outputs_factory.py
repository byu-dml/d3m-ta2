import typing
from generated_grpc import pipeline_pb2


class StepOutputsFactory:

    @staticmethod
    def to_protobuf(outputs: typing.List[str]) -> typing.List[pipeline_pb2.StepOutput]:
        protobuf_outputs = []
        for output_str in outputs:
            protobuf_output = pipeline_pb2.StepOutput(id=output_str)
            protobuf_outputs.append(protobuf_output)
        return protobuf_outputs
