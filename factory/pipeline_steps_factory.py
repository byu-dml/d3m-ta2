import typing
from generated_grpc import pipeline_pb2
from d3m.metadata import pipeline as pipeline_module
from factory.primitive_pipeline_step_factory import PrimitivePipelineStepFactory


class PipelineStepsFactory:

    @staticmethod
    def to_protobuf_steps(steps: typing.List[pipeline_module.StepBase]) -> typing.List[pipeline_pb2.PipelineDescriptionStep]:
        protobuf_pipeline_description_steps = []
        for step in steps:
            protobuf_pipeline_description_step = None
            if isinstance(step, pipeline_module.PrimitiveStep):
                protobuf_primitive_pipeline_description_step = PrimitivePipelineStepFactory.to_protobuf(step)
                protobuf_pipeline_description_step = pipeline_pb2.PipelineDescriptionStep(primitive=protobuf_primitive_pipeline_description_step)
            elif isinstance(step, pipeline_module.SubpipelineStep):
                pass
            elif isinstance(step, pipeline_module.PlaceholderStep):
                pass
            protobuf_pipeline_description_steps.append(protobuf_pipeline_description_step)
        return protobuf_pipeline_description_steps

    @staticmethod
    def from_protobuf_steps(protobuf_steps: typing.List[pipeline_pb2.PipelineDescriptionStep]) -> typing.List[pipeline_module.StepBase]:
        pipeline_steps = []
        for protobuf_step in protobuf_steps:
            if protobuf_step.WhichOneof('step') == 'primitive':
                step = PrimitivePipelineStepFactory.from_protobuf(protobuf_step.primitive)
            elif protobuf_step.WhichOneof('step') == 'pipeline':
                pass
            elif protobuf_step.WhichOneof('step') == 'placeholder':
                pass
            pipeline_steps.append(step)
        return pipeline_steps

