from d3m.metadata import pipeline as pipeline_module


class PrimitiveStepHyperparamFactory:

    @staticmethod
    def get_protobuf_step(primitive_step_argument: pipeline_module.PrimitiveStep):
        primitive_step_argument.arguments

