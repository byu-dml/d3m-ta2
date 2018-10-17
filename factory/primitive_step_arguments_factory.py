from d3m.metadata import pipeline as pipeline_module
import typing
from wrapper.pipeline.container_argument import ContainerArgument
from generated_grpc import pipeline_pb2
from wrapper.pipeline.data_argument import DataArgument


class PrimitiveStepArgumentsFactory:

    @staticmethod
    def to_protobuf_arguments(primitive_step_arguments: typing.Dict[str, typing.Dict[str, typing.Any]]) -> typing.Dict[str, pipeline_pb2.PrimitiveStepArgument]:
        protobuf_arguments = {}
        for name, argument in primitive_step_arguments.items():
            if argument['type'] == pipeline_module.ArgumentType.CONTAINER:
                container = ContainerArgument(argument['data']).to_protobuf()
                protobuf_arguments[name] = pipeline_pb2.PrimitiveStepArgument(container=container)
            elif argument['type'] == pipeline_module.ArgumentType.DATA:
                data = DataArgument(argument['data']).to_protobuf()
                protobuf_arguments[name] = pipeline_pb2.PrimitiveStepArgument(data=data)
        return protobuf_arguments

    @staticmethod
    def from_protobuf_arguments(protobuf_arguments: typing.Dict[str, pipeline_pb2.PrimitiveStepArgument]) -> typing.List[dict]:
        arguments: typing.List[dict] = []
        for name, protobuf_argument in protobuf_arguments.items():
            argument_type_str = protobuf_argument.WhichOneof('argument')
            data_reference = getattr(protobuf_argument, argument_type_str).data
            argument_type = pipeline_module.ArgumentType[argument_type_str.upper()]
            argument = {'name': name, 'argument_type': argument_type, 'data_reference': data_reference}
            arguments.append(argument)
        return arguments
