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
        primitive = Primitive(primitive_description).to_protobuf()
        protobuf_primitive_step_arguments = PrimitiveStepArgumentsFactory.to_protobuf_arguments(step.arguments)
        protobuf_primitive_step_outputs = StepOutputsFactory.to_protobuf(step.outputs)
        protobuf_primitive_step_hyperparams = PrimitiveStepHyperparamFactory.to_protobuf_hyperparams(step.hyperparams)
        # TODO: implementation for users field (optional)
        protobuf_primitive_pipeline_description_step = pipeline_pb2.PrimitivePipelineDescriptionStep(primitive=primitive,
                                                                                            arguments=protobuf_primitive_step_arguments,
                                                                                            outputs=protobuf_primitive_step_outputs,
                                                                                            hyperparams=protobuf_primitive_step_hyperparams
                                                                                            )
        return protobuf_primitive_pipeline_description_step

    @staticmethod
    def from_protobuf(protobuf_primitive_step: pipeline_pb2.PrimitivePipelineDescriptionStep) -> pipeline_module.PrimitiveStep:
        protobuf_primitive = protobuf_primitive_step.primitive
        primitive_description = Primitive.from_protobuf(protobuf_primitive)
        primitive_step = pipeline_module.PrimitiveStep(primitive_description=primitive_description)

        # add arguments to primitive step
        primitive_step_arguments = PrimitiveStepArgumentsFactory.from_protobuf_arguments(protobuf_primitive_step.arguments)
        for argument in primitive_step_arguments:
            primitive_step.add_argument(name=argument['name'], argument_type=argument['argument_type'], data_reference=argument['data_reference'])

        # add outputs to primitive step
        primitive_step_outputs = StepOutputsFactory.from_protobuf(protobuf_primitive_step.outputs)
        for output in primitive_step_outputs:
            primitive_step.add_output(output)

        # add hyperparams to primitive step
        primitive_step_hyperparams = PrimitiveStepHyperparamFactory.from_protobuf_hyperparams(protobuf_primitive_step.hyperparams)
        for hyperparam in primitive_step_hyperparams:
            primitive_step.add_hyperparameter(name=hyperparam['name'], argument_type=hyperparam['argument_type'], data=hyperparam['data'])

        # TODO: implementation for users field (optional)

        return primitive_step