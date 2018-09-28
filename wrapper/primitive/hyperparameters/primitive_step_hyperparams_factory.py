from generated_grpc import pipeline_pb2
from d3m.metadata import pipeline as pipeline_module
import typing
from wrapper.primitive.container_argument import ContainerArgument
from wrapper.primitive.data_argument import DataArgument
from wrapper.primitive.hyperparameters.primitive_argument import PrimitiveArgument
from wrapper.primitive.hyperparameters.value_argument import ValueArgument


class PrimitiveStepHyperparamFactory:

    @staticmethod
    def get_protobuf_hyperparams(primitive_step_hyperparams: typing.Dict[str, typing.Dict[str, typing.Any]]):
        protobuf_hyperparams = {}
        for name, hyperparam in primitive_step_hyperparams.items():
            if hyperparam['type'] == pipeline_module.ArgumentType.CONTAINER:
                container = ContainerArgument(hyperparam['data']).to_protobuf()
                protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(container=container)
            elif hyperparam['type'] == pipeline_module.ArgumentType.DATA:
                data = DataArgument(hyperparam['data']).to_protobuf()
                protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(data=data)
            elif hyperparam['type'] == pipeline_module.ArgumentType.PRIMITIVE:
                primitive = PrimitiveArgument(hyperparam['data']).to_protobuf()
                protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(primitive=primitive)
            elif hyperparam['type'] == pipeline_module.ArgumentType.VALUE:
                value = ValueArgument(hyperparam['data']).to_protobuf()
                protobuf_hyperparams[name] = pipeline_pb2.PrimitiveStepHyperparameter(value=value)
        return protobuf_hyperparams


