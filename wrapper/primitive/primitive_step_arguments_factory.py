from d3m.metadata import pipeline as pipeline_module
import typing
from wrapper.primitive.container_argument import ContainerArgument
from generated_grpc import pipeline_pb2
from wrapper.primitive.data_argument import DataArgument


class PrimitiveStepArgumentsFactory:

    @staticmethod
    def get_protobuf_arguments(primitive_step_arguments: typing.Dict[str, typing.Dict[str, typing.Any]]):
        protobuf_arguments = {}
        for name, argument in primitive_step_arguments.items():
            if argument['type'] == pipeline_module.ArgumentType.CONTAINER:
                container = ContainerArgument(argument['data']).to_protobuf()
                protobuf_arguments[name] = pipeline_pb2.PrimitiveStepArgument(container=container)
            elif argument['type'] == pipeline_module.ArgumentType.DATA:
                data = DataArgument(argument['data']).to_protobuf()
                protobuf_arguments[name] = pipeline_pb2.PrimitiveStepArgument(data=data)
        return protobuf_arguments
