from generated_grpc import pipeline_pb2


class ContainerArgument:

    def __init__(self, data):
        self.data = data

    def to_protobuf(self):
        return pipeline_pb2.ContainerArgument(data=self.data)

    @staticmethod
    def from_protobuf(protobuf_container: pipeline_pb2.ContainerArgument) -> str:
        return protobuf_container.data




