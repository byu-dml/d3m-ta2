from factory import pipeline_description_factory
from d3m.metadata import pipeline as pipeline_module
from generated_grpc import pipeline_pb2


class TestPipelineConversion:

    @staticmethod
    def test_pipeline_to_protobuf_to_pipeline(random_forest_pipeline: pipeline_module.Pipeline):
        protobuf_pipeline: pipeline_pb2.PipelineDescription = pipeline_description_factory.PipelineDescriptionFactory.to_protobuf_pipeline_description(random_forest_pipeline)
        converted_pipeline: pipeline_module.Pipeline = pipeline_description_factory.PipelineDescriptionFactory.from_protobuf_pipeline_description(protobuf_pipeline)
        assert TestPipelineConversion.equal(random_forest_pipeline, converted_pipeline)

    @staticmethod
    def equal(p1: pipeline_module.Pipeline, p2: pipeline_module.Pipeline):
        assert p1.id == p2.id
        assert p1.context == p2.context
        assert p1.name == p2.name
        assert p1.description == p2.description
        assert TestPipelineConversion.equal_inputs(p1, p2)
        assert TestPipelineConversion.equal_outputs(p1, p2)
        assert TestPipelineConversion.equal_steps(p1, p2)
        return True

    @staticmethod
    def equal_inputs(p1: pipeline_module.Pipeline, p2: pipeline_module.Pipeline):
        assert len(p1.inputs) == len(p2.inputs)
        for i in range(len(p1.inputs)):
            assert p1.inputs[i] == p2.inputs[i]
        return True

    @staticmethod
    def equal_outputs(p1: pipeline_module.Pipeline, p2: pipeline_module.Pipeline):
        assert len(p1.outputs) == len(p2.outputs)
        for i in range(len(p1.outputs)):
            assert p1.outputs[i] == p2.outputs[i]
        return True

    @staticmethod
    def equal_steps(p1: pipeline_module.Pipeline, p2: pipeline_module.Pipeline):
        assert len(p1.steps) == len(p2.steps)
        for i in range(len(p1.steps)):
            p1_step, p2_step = p1.steps[i], p2.steps[i]
            assert type(p1_step) == type(p2_step)
            if isinstance(p1_step, pipeline_module.PrimitiveStep):
                # dictionaries
                assert p1_step.primitive_description == p2_step.primitive_description
                # list of strings
                assert p1_step.outputs == p2_step.outputs
                # dictionaries of strings to dictionaries
                assert p1_step.hyperparams == p2_step.hyperparams
                # dictionaries of strings to dictionaries
                assert p1_step.arguments == p2_step.arguments
        return True



