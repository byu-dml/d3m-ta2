import typing
import collections

from generated_grpc import pipeline_pb2
from d3m.metadata import pipeline as pipeline_module

from wrapper.primitive.container_argument import ContainerArgument
from wrapper.primitive.data_argument import DataArgument
from wrapper.primitive.hyperparameters.primitive_argument import PrimitiveArgument
from wrapper.primitive.hyperparameters.value_argument import ValueArgument


class PrimitiveStepHyperparamFactory:

    @staticmethod
    def get_protobuf_hyperparams(primitive_step_hyperparams: typing.Dict[str, typing.Dict[str, typing.Any]]):
        protobuf_hyperparams = {}
        for name, hyperparam in primitive_step_hyperparams.items():
            type_ = hyperparam['type']
            print(type_)
            data = hyperparam['data']
            if type_ == pipeline_module.ArgumentType.CONTAINER:
                container = ContainerArgument(data).to_protobuf()
                protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(container=container)
            elif type_ == pipeline_module.ArgumentType.DATA:
                data = DataArgument(data).to_protobuf()
                protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(data=data)
            elif type_ == pipeline_module.ArgumentType.PRIMITIVE:
                primitive = PrimitiveArgument(data).to_protobuf()
                protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(primitive=primitive)
            elif type_ == pipeline_module.ArgumentType.VALUE:
                value = ValueArgument(data).to_protobuf()
                protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(value=value)
            elif isinstance(data, collections.Iterable):
                data_set: typing.Set[str] = set([d for d in data if isinstance(d, str)])
                primitives_set: typing.Set[int] = set([d for d in data if isinstance(d, int)])
                if len(data_set) > 0:
                    protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(data_set=data_set)
                else:
                    protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(primitive_set=primitives_set)

        return protobuf_hyperparams


