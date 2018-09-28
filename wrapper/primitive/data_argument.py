from generated_grpc import pipeline_pb2


class DataArgument:

    def __init__(self, data):
        self.data = data

    def to_protobuf(self):
        return pipeline_pb2.DataArgument(data=self.data)