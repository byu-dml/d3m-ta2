from generated_grpc import pipeline_pb2
from d3m.metadata import pipeline as pipeline_module
import typing
from wrapper.primitive.primitive import Primitive
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
from util.timestamp_util import TimestampUtil


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
                primitive_description = step.primitive_description
                primitive = Primitive.get_primitive_from_json(primitive_description)
                arguments = step.arguments
                primitive_step_arguments = PipelineDescription.get_primitive_step_arguments(arguments)
                outputs = step.outputs
                primitive_step_outputs = PipelineDescription.get_primitive_step_outputs(outputs)
                hyperparams = step.hyperparams
                primitive_step_hyperparams = PipelineDescription.get_primitive_step_hyperparams(hyperparams)

                # TODO: hyperparams field
                # TODO: users field (optional)

                primitive_description_step = pipeline_pb2.PrimitivePipelineDescriptionStep(primitive=primitive,
                                                                                           arguments=primitive_step_arguments,
                                                                                           outputs=primitive_step_outputs,
                                                                                           hyperparams=primitive_step_hyperparams
                                                                                           )

                pipeline_description_step = pipeline_pb2.PipelineDescriptionStep(primitive=primitive_description_step)
                steps.append(pipeline_description_step)
        return steps

    @staticmethod
    def get_primitive_step_hyperparams(hyperparams: dict) -> typing.Dict[str, pipeline_pb2.PrimitiveStepHyperparameter]:
        primitive_step_hyperparams = {}
        for key, hyperparam in hyperparams.items():
            protobuf_param = pipeline_pb2.PrimitiveStepHyperparameter(hyperparam)
            primitive_step_hyperparams[key] = protobuf_param
            # data = hyperparam['data']
            # type = hyperparam['type']
            # if type == pipeline_module.ArgumentType.CONTAINER:
            #     pass
            # if type == pipeline_module.ArgumentType.DATA:
            #     pass
            # if type == pipeline_module.ArgumentType.PRIMITIVE:
            #     pass
            # if type == pipeline_module.ArgumentType.VALUE:
            #     pass
        return primitive_step_hyperparams

    @staticmethod
    def get_primitive_step_outputs(outputs: typing.List[str]) -> typing.List[pipeline_pb2.StepOutput]:
        primitive_step_outputs = []
        for output in outputs:
            primitive_step_output = pipeline_pb2.StepOutput(id=output)
            primitive_step_outputs.append(primitive_step_output)
        return primitive_step_outputs

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
                for name, protobuf_argument in protobuf_primitive_step.arguments.items():
                    argument_type_str = protobuf_argument.WhichOneof('argument')
                    data_reference = getattr(protobuf_argument, argument_type_str).data
                    argument_type = pipeline_module.ArgumentType[argument_type_str.upper()]
                    step.add_argument(name=name, argument_type=argument_type, data_reference=data_reference)

                # add hyperparams to primitive step
                # for name, protobuf_hyperparam in protobuf_primitive_step.hyperparams.items():
                #     if protobuf_hyperparam.WhichOneof('argument') == 'container':
                #         argument_type = pipeline_module.ArgumentType.CONTAINER
                #         data = protobuf_hyperparam.container.data
                #     elif protobuf_hyperparam.WhichOneof('argument') == 'data':
                #         argument_type = pipeline_module.ArgumentType.DATA
                #         data = protobuf_hyperparam.data.data
                #     elif protobuf_hyperparam.WhichOneof('argument') == 'primitive':
                #         argument_type = pipeline_module.ArgumentType.PRIMITIVE
                #         data = protobuf_hyperparam.primitive.data
                #     elif protobuf_hyperparam.WhichOneof('argument') == 'value':
                #         argument_type = pipeline_module.ArgumentType.VALUE
                #         data = protobuf_hyperparam.value.data
                #
                #     step.add_hyperparameter(name=name, argument_type=type, data=data)

                # add outputs to primitive
                for output in protobuf_primitive_step.outputs:
                    step.add_output(output.id)

                # TODO: add users field (options)

                pipeline.add_step(step)

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

