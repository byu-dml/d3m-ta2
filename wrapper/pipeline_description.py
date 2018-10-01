from generated_grpc import pipeline_pb2
from d3m.metadata import pipeline as pipeline_module
import typing
from wrapper.primitive.primitive import Primitive
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
from util.timestamp_util import TimestampUtil
from wrapper.primitive.hyperparameters.primitive_step_hyperparams_factory import PrimitiveStepHyperparamFactory
from wrapper.primitive.primitive_step_arguments_factory import PrimitiveStepArgumentsFactory
from pprint import pprint


class PipelineDescription:

    @staticmethod
    def pipeline_to_protobuf_pipeline(pipeline: pipeline_module.Pipeline) -> pipeline_pb2.PipelineDescription:
        pipeline_id = pipeline.id
        pipeline_created = PipelineDescription.get_created_protobuf(pipeline)
        pipeline_context = PipelineDescription.pipeline_context_enum_to_proto_pipeline_context_enum(pipeline.context)
        pipeline_name = pipeline.name
        pipeline_description = pipeline.description

        pipeline_inputs: typing.List[dict] = PipelineDescription.get_pipeline_inputs(pipeline)
        pipeline_outputs = PipelineDescription.get_pipeline_outputs(pipeline)
        pipeline_steps: typing.List[pipeline_pb2.PipelineDescriptionStep] = PipelineDescription.get_pipeline_steps(
            pipeline)

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
    def get_pipeline_outputs(pipeline: pipeline_module.Pipeline) -> typing.List[pipeline_pb2.PipelineDescriptionOutput]:
        outputs = []
        for output in pipeline.outputs:
            description_output = pipeline_pb2.PipelineDescriptionOutput(name=output['name'], data=output['data'])
            outputs.append(description_output)
        return outputs

    @staticmethod
    def get_pipeline_inputs(pipeline: pipeline_module.Pipeline) -> typing.List[pipeline_pb2.PipelineDescriptionInput]:
        pipeline_description_inputs = []
        for input_ in pipeline.inputs:
            input_name = input_['name']
            description_input = pipeline_pb2.PipelineDescriptionInput(name=input_name)
            pipeline_description_inputs.append(description_input)

        return pipeline_description_inputs

    @staticmethod
    def get_pipeline_steps(pipeline: pipeline_module.Pipeline) -> typing.List[pipeline_pb2.PipelineDescriptionStep]:
        steps = []
        for step in pipeline.steps:
            if isinstance(step, pipeline_module.PrimitiveStep):
                PipelineDescription.get_pipeline_description_steps(step, steps)
        return steps

    @staticmethod
    def get_pipeline_description_steps(step, steps):
        primitive_description = step.primitive_description
        primitive = Primitive.get_primitive_from_json(primitive_description)
        primitive_step_arguments = PrimitiveStepArgumentsFactory.to_protobuf_arguments(step.arguments)
        primitive_step_outputs = PipelineDescription.get_primitive_step_outputs(step.outputs)
        primitive_step_hyperparams = PrimitiveStepHyperparamFactory.to_protobuf_hyperparams(step.hyperparams)
        # TODO: users field (optional)
        primitive_description_step = pipeline_pb2.PrimitivePipelineDescriptionStep(primitive=primitive,
                                                                                   arguments=primitive_step_arguments,
                                                                                   outputs=primitive_step_outputs,
                                                                                   hyperparams=primitive_step_hyperparams
                                                                                   )
        pipeline_description_step = pipeline_pb2.PipelineDescriptionStep(primitive=primitive_description_step)
        steps.append(pipeline_description_step)

    @staticmethod
    def get_primitive_step_outputs(outputs: typing.List[str]) -> typing.List[pipeline_pb2.StepOutput]:
        primitive_step_outputs = []
        for output in outputs:
            primitive_step_output = pipeline_pb2.StepOutput(id=output)
            primitive_step_outputs.append(primitive_step_output)
        return primitive_step_outputs

    @staticmethod
    def get_created_protobuf(pipeline: pipeline_module.Pipeline) -> Timestamp:
        created_datetime: datetime.datetime = pipeline.created
        return TimestampUtil.get_proto_timestamp(created_datetime)

    @staticmethod
    def get_pipeline_from_protobuf_pipeline(protobuf_pipeline: pipeline_pb2.PipelineDescription) -> pipeline_module.Pipeline:
        id = protobuf_pipeline.id
        # source
        # created
        context = PipelineDescription.proto_pipeline_context_enum_to_pipeline_context_enum(protobuf_pipeline.context)
        name = protobuf_pipeline.name
        description = protobuf_pipeline.description
        # TODO: users field (optional)
        pipeline = pipeline_module.Pipeline(pipeline_id=id, context=context, name=name, description=description)

        # add inputs to pipeline
        for input in protobuf_pipeline.inputs:
            pipeline.add_input(name=input.name)

        # add steps to pipeline
        for protobuf_step in protobuf_pipeline.steps:
            print("GOING THROUGH PROTOBUF STEPS")
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

                # TODO: add users field (options)

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

