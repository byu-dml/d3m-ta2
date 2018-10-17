from generated_grpc import pipeline_pb2
from d3m.metadata import pipeline as pipeline_module
import typing
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
from util.timestamp_util import TimestampUtil
from factory.pipeline_inputs_factory import PipelineInputsFactory
from factory.pipeline_outputs_factory import PipelineOutputsFactory
from factory.pipeline_steps_factory import PipelineStepsFactory


class PipelineDescriptionFactory:

    #
    # --------------------------------  To Protobuf -----------------------------------------
    #

    @staticmethod
    def to_protobuf_pipeline_description(pipeline: pipeline_module.Pipeline) -> pipeline_pb2.PipelineDescription:
        pipeline_id = pipeline.id
        # TODO: implementation for source field (optional)
        pipeline_created = PipelineDescriptionFactory.get_created_protobuf(pipeline)
        pipeline_context = PipelineDescriptionFactory.pipeline_context_enum_to_proto_pipeline_context_enum(pipeline.context)
        pipeline_name = pipeline.name
        pipeline_description = pipeline.description
        # TODO: implementation for users field (optional)
        pipeline_inputs: typing.List[pipeline_pb2.PipelineDescriptionInput] = PipelineInputsFactory.to_protobuf_inputs(pipeline.inputs)
        pipeline_outputs: typing.List[pipeline_pb2.PipelineDescriptionOutput] = PipelineOutputsFactory.to_protobuf_outputs(pipeline.outputs)
        pipeline_steps: typing.List[pipeline_pb2.PipelineDescriptionStep] = PipelineStepsFactory.to_protobuf_steps(pipeline.steps)

        return pipeline_pb2.PipelineDescription(id=pipeline_id,
                                                created=pipeline_created,
                                                context=pipeline_context,
                                                name=pipeline_name,
                                                description=pipeline_description,
                                                inputs=pipeline_inputs,
                                                outputs=pipeline_outputs,
                                                steps=pipeline_steps
                                                )

    @staticmethod
    def pipeline_context_enum_to_proto_pipeline_context_enum(context: pipeline_module.PipelineContext) -> int:
        switcher = {
            pipeline_module.PipelineContext.PRETRAINING: pipeline_pb2.PRETRAINING,
            pipeline_module.PipelineContext.TESTING: pipeline_pb2.TESTING,
            pipeline_module.PipelineContext.EVALUATION: pipeline_pb2.EVALUATION,
            pipeline_module.PipelineContext.PRODUCTION: pipeline_pb2.PRODUCTION
        }
        return switcher.get(context, pipeline_pb2.PIPELINE_CONTEXT_UNKNOWN)

    @staticmethod
    def get_created_protobuf(pipeline: pipeline_module.Pipeline) -> Timestamp:
        created_datetime: datetime.datetime = pipeline.created
        return TimestampUtil.get_proto_timestamp(created_datetime)

    #
    # --------------------------------  From Protobuf -----------------------------------------
    #

    @staticmethod
    def from_protobuf_pipeline_description(protobuf_pipeline: pipeline_pb2.PipelineDescription) -> pipeline_module.Pipeline:
        pipeline_id = protobuf_pipeline.id
        # TODO: implementation for source field (optional)
        # TODO: implementation for created field
        # created = TimestampUtil.from_proto_timestamp(protobuf_pipeline.created)
        context = PipelineDescriptionFactory.proto_pipeline_context_enum_to_pipeline_context_enum(protobuf_pipeline.context)
        name = protobuf_pipeline.name
        description = protobuf_pipeline.description
        # TODO: implementation for users field (optional)
        pipeline = pipeline_module.Pipeline(pipeline_id=pipeline_id, context=context, name=name, description=description)

        # add inputs to pipeline
        pipeline_inputs: typing.List[str] = PipelineInputsFactory.from_protobuf_inputs(protobuf_pipeline.inputs)
        for input in pipeline_inputs:
            pipeline.add_input(name=input)

        # add steps to pipeline
        pipeline_steps: typing.List[pipeline_module.StepBase] = PipelineStepsFactory.from_protobuf_steps(protobuf_pipeline.steps)
        for step in pipeline_steps:
            pipeline.add_step(step=step)

        # add outputs to pipeline
        pipeline_outputs: typing.List[dict] = PipelineOutputsFactory.from_protobuf_outputs(protobuf_pipeline.outputs)
        for output in pipeline_outputs:
            pipeline.add_output(data_reference=output['data'], name=output['name'])

        return pipeline

    @staticmethod
    def proto_pipeline_context_enum_to_pipeline_context_enum(context: pipeline_pb2.PipelineContext) -> pipeline_module.PipelineContext:
        switcher = {
            1: pipeline_module.PipelineContext.PRETRAINING,
            2: pipeline_module.PipelineContext.TESTING,
            3: pipeline_module.PipelineContext.EVALUATION,
            4: pipeline_module.PipelineContext.PRODUCTION
        }
        return switcher.get(context, 0)

