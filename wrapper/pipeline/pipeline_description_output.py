from generated_grpc import pipeline_pb2


class PipelineDescriptionOutput:

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def to_protobuf(self) -> pipeline_pb2.PipelineDescriptionOutput:
        return pipeline_pb2.PipelineDescriptionOutput(name=self.name, data=self.data)

    # @staticmethod
    # def from_protobuf(protobuf_pipeline_description_output: pipeline_pb2.PipelineDescriptionOutput):
    #     return protobuf_pipeline_description_output.name
