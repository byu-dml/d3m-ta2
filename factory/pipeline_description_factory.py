from generated_grpc import pipeline_pb2
from d3m.metadata import pipeline as pipeline_module
import typing
from wrapper.primitive.primitive import Primitive
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
from util.timestamp_util import TimestampUtil
from factory.primitive_step_hyperparams_factory import PrimitiveStepHyperparamFactory
from factory.primitive_step_arguments_factory import PrimitiveStepArgumentsFactory
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
        pipeline_created = PipelineDescriptionFactory.get_created_protobuf(pipeline)
        pipeline_context = PipelineDescriptionFactory.pipeline_context_enum_to_proto_pipeline_context_enum(pipeline.context)
        pipeline_name = pipeline.name
        pipeline_description = pipeline.description

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
        # source
        # created
        context = PipelineDescriptionFactory.proto_pipeline_context_enum_to_pipeline_context_enum(protobuf_pipeline.context)
        name = protobuf_pipeline.name
        description = protobuf_pipeline.description
        # TODO: users field (optional)
        pipeline = pipeline_module.Pipeline(pipeline_id=pipeline_id, context=context, name=name, description=description)

        # add inputs to pipeline
        for input in protobuf_pipeline.inputs:
            pipeline.add_input(name=input.name)

        # add steps to pipeline
        for protobuf_step in protobuf_pipeline.steps:
            if protobuf_step.WhichOneof('step') == 'primitive':
                protobuf_primitive_step = protobuf_step.primitive
                protobuf_primitive_description = protobuf_primitive_step.primitive
                primitive_description = {'id': protobuf_primitive_description.id,
                                         'version': protobuf_primitive_description.version,
                                         'python_path': protobuf_primitive_description.python_path,
                                         'name': protobuf_primitive_description.name,
                                         'digest': protobuf_primitive_description.digest
                                        }
                # initialize primitive step with primitive description
                step = pipeline_module.PrimitiveStep(primitive_description=primitive_description)

                # add arguments to primitive step
                PrimitiveStepArgumentsFactory.from_protobuf_arguments(protobuf_primitive_step.arguments, step)

                # add hyperparams to primitive step
                PrimitiveStepHyperparamFactory.from_protobuf_hyperparams(protobuf_primitive_step.hyperparams, step)

                # add outputs to primitive step
                for output in protobuf_primitive_step.outputs:
                    step.add_output(output.id)

                # TODO: add users field (optional)

                pipeline.add_step(step)

        for output in protobuf_pipeline.outputs:
            pipeline.add_output(output.data, output.name)

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

