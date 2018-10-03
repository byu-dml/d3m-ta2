import typing

from generated_grpc import pipeline_pb2
from d3m.metadata import pipeline as pipeline_module

from wrapper.pipeline.container_argument import ContainerArgument
from wrapper.pipeline.data_argument import DataArgument
from wrapper.pipeline.primitive_argument import PrimitiveArgument
from wrapper.pipeline.value_argument import ValueArgument


class PrimitiveStepHyperparamFactory:

    @staticmethod
    def to_protobuf_hyperparams(primitive_step_hyperparams: typing.Dict[str, typing.Dict[str, typing.Any]]) -> typing.Dict[str, pipeline_pb2.PrimitiveStepHyperparameter]:
        protobuf_hyperparams = {}
        for name, hyperparam in primitive_step_hyperparams.items():
            type_ = hyperparam['type']
            data = hyperparam['data']
            if type_ == pipeline_module.ArgumentType.CONTAINER:
                container = ContainerArgument(data).to_protobuf()
                protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(container=container)
            elif type_ == pipeline_module.ArgumentType.DATA:
                if isinstance(data, typing.List):
                    data_set = pipeline_pb2.DataArguments(data=data)
                    protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(data_set=data_set)
                else:
                    data = DataArgument(data).to_protobuf()
                    protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(data=data)
            elif type_ == pipeline_module.ArgumentType.PRIMITIVE:
                if isinstance(data, typing.List):
                    primitives_set = pipeline_pb2.PrimitiveArguments(data=data)
                    protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(primitive_set=primitives_set)
                else:
                    primitive = PrimitiveArgument(data).to_protobuf()
                    protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(primitive=primitive)
            elif type_ == pipeline_module.ArgumentType.VALUE:
                value = ValueArgument(data).to_protobuf()
                protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(value=value)

        return protobuf_hyperparams

    @staticmethod
    def from_protobuf_hyperparams(protobuf_hyperparams: typing.Dict[str, pipeline_pb2.PrimitiveStepHyperparameter], step: pipeline_module.PrimitiveStep) -> None:
        for name, protobuf_hyperparam in protobuf_hyperparams.items():
            argument_type_str = protobuf_hyperparam.WhichOneof('argument')
            argument_type = pipeline_module.ArgumentType[argument_type_str.upper()]
            if argument_type_str == 'container':
                data = ContainerArgument.from_protobuf(protobuf_hyperparam.container)
            elif argument_type_str == 'data':
                data = DataArgument.from_protobuf(protobuf_hyperparam.data)
            elif argument_type_str == 'primitive':
                data = PrimitiveArgument.from_protobuf(protobuf_hyperparam.primitive)
            elif argument_type_str == 'value':
                data = ValueArgument.from_protobuf(protobuf_hyperparam.value)
            elif argument_type_str == 'data_set':
                data = protobuf_hyperparam.data_set.data
            elif argument_type_str == 'primitive_set':
                data = protobuf_hyperparam.primitive_set.data
            step.add_hyperparameter(name=name, argument_type=argument_type, data=data)


