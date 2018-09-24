from generated_grpc import pipeline_pb2
from d3m.metadata import pipeline as pipeline_module
import typing
from wrapper.primitive import Primitive
from google.protobuf.timestamp_pb2 import Timestamp
import datetime


class PipelineDescription:

    @staticmethod
    def pipeline_to_protobuf_pipeline(pipeline: pipeline_module.Pipeline) -> pipeline_pb2.PipelineDescription:
        pipeline_id = pipeline.id
        pipeline_created = PipelineDescription.get_protobuf_timestamp(pipeline)
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
                primitive_description = step.primitive_description
                primitive = Primitive.get_primitive_from_json(primitive_description)
                arguments = step.arguments
                primitive_step_arguments = PipelineDescription.get_primitive_step_arguments(arguments)

                primitive_description_step = pipeline_pb2.PrimitivePipelineDescriptionStep(primitive=primitive,
                                                                                           arguments=primitive_step_arguments)

                pipeline_description_step = pipeline_pb2.PipelineDescriptionStep(primitive=primitive_description_step)
                steps.append(pipeline_description_step)
        return steps

    @staticmethod
    def get_primitive_step_arguments(arguments: dict) -> typing.Dict[str, pipeline_pb2.PrimitiveStepArgument]:
        primitive_step_arguments = {}
        for key, argument in arguments.items():
            data = argument['data']
            type_ = argument['type']

            primitive_step_argument = None
            if type_ == pipeline_module.ArgumentType.CONTAINER:
                container_argument = pipeline_pb2.ContainerArgument(data=data)
                primitive_step_argument = pipeline_pb2.PrimitiveStepArgument(container=container_argument)
            elif type_ == pipeline_module.ArgumentType.DATA:
                data_argument = pipeline_pb2.DataArgument(date=data)
                primitive_step_argument = pipeline_pb2.PrimitiveStepArgument(data=data_argument)
            else:
                raise RuntimeError(f'''Invalid primitive step argument type {type_}. 
                Accepted types are: {pipeline_module.ArgumentType.CONTAINER} and {pipeline_module.ArgumentType.DATA}''')

            primitive_step_arguments[key] = primitive_step_argument

        return primitive_step_arguments

    @staticmethod
    def get_protobuf_timestamp(pipeline: pipeline_module.Pipeline) -> Timestamp:
        created_datetime: datetime.datetime = pipeline.created
        created_datetime = created_datetime.replace(tzinfo=None)
        created: Timestamp = Timestamp()
        created.FromDatetime(created_datetime)
        return created

    @staticmethod
    def get_pipeline_from_protobuf_pipeline(protobuf_pipeline: pipeline_pb2.PipelineDescription) -> pipeline_module.Pipeline:
        id = protobuf_pipeline.id
        context = PipelineDescription.proto_pipeline_context_enum_to_pipeline_context_enum(protobuf_pipeline.context)
        # created
        name = protobuf_pipeline.name
        description = protobuf_pipeline.description

        pipeline = pipeline_module.Pipeline(pipeline_id=id, context=context, name=name, description=description)

        for input in protobuf_pipeline.inputs:
            pipeline.add_input(input.name)

        # for protobuf_step in protobuf_pipeline.steps:
        #
        # for output in protobuf_pipeline.outputs:
        #     pipeline.add_output(output.data, output.name)

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

