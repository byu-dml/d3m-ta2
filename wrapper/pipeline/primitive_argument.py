from generated_grpc import pipeline_pb2


class PrimitiveArgument:

    def __init__(self, data):
        self.data = data

    def to_protobuf(self):
        return pipeline_pb2.PrimitiveArgument(data=self.data)

    @staticmethod
    def from_protobuf(protobuf_primitive: pipeline_pb2.PrimitiveArgument) -> int:
        return protobuf_primitive.data
