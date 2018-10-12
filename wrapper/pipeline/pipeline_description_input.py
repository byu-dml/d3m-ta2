from generated_grpc import pipeline_pb2


class PipelineDescriptionInput:

    def __init__(self, name):
        self.name = name

    def to_protobuf(self) -> pipeline_pb2.PipelineDescriptionInput:
        return pipeline_pb2.PipelineDescriptionInput(name=self.name)

    @staticmethod
    def from_protobuf(protobuf_pipeline_description_input: pipeline_pb2.PipelineDescriptionInput):
        return protobuf_pipeline_description_input.name
