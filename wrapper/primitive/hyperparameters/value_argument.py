from generated_grpc import pipeline_pb2


class ValueArgument:

    def __init__(self, data):
        self.data = data

    def to_protobuf(self):
        # TODO: need to find out more detail on what kind of value data this is in order to instantiate the correct subtype
        return pipeline_pb2.ValueArgument(data=self.data)