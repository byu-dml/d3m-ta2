from generated_grpc import pipeline_pb2, value_pb2
from wrapper.value.value_raw import ValueRaw


class ValueArgument:

    def __init__(self, data):
        self.data = data

    def to_protobuf(self):
        value_raw = ValueRaw(self.data)
        value = value_pb2.Value(raw=value_raw.to_protobuf())
        return pipeline_pb2.ValueArgument(data=value)
