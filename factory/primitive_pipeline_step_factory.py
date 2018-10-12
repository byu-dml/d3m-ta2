from d3m.metadata import pipeline as pipeline_module
from generated_grpc import pipeline_pb2
from wrapper.primitive.primitive import Primitive
from factory.primitive_step_arguments_factory import PrimitiveStepArgumentsFactory
from factory.primitive_step_hyperparams_factory import PrimitiveStepHyperparamFactory
from factory.step_outputs_factory import StepOutputsFactory

class PrimitivePipelineStepFactory:

    @staticmethod
    def to_protobuf(step: pipeline_module.PrimitiveStep) -> pipeline_pb2.PrimitivePipelineDescriptionStep:
        primitive_description = step.primitive_description
        primitive = Primitive.get_primitive_from_json(primitive_description)
        protobuf_primitive_step_arguments = PrimitiveStepArgumentsFactory.to_protobuf_arguments(step.arguments)
        protobuf_primitive_step_outputs = StepOutputsFactory.to_protobuf(step.outputs)
        protobuf_primitive_step_hyperparams = PrimitiveStepHyperparamFactory.to_protobuf_hyperparams(step.hyperparams)
        # TODO: users field (optional)
        protobuf_primitive_pipeline_description_step = pipeline_pb2.PrimitivePipelineDescriptionStep(primitive=primitive,
                                                                                            arguments=protobuf_primitive_step_arguments,
                                                                                            outputs=protobuf_primitive_step_outputs,
                                                                                            hyperparams=protobuf_primitive_step_hyperparams
                                                                                            )
        return protobuf_primitive_pipeline_description_step
