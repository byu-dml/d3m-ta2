from generated_grpc import pipeline_pb2, value_pb2
from wrapper.value.value_raw import ValueRaw
import typing


class ValueArgument:

    def __init__(self, data):
        self.data = data

    def to_protobuf(self):
        # making assumption that the self.data is a raw value
        # TODO: add functionality for when self.data is an 'error', 'dataset_uri', or 'csv_uri'
        value_raw = ValueRaw(self.data)
        value = value_pb2.Value(raw=value_raw.to_protobuf())
        return pipeline_pb2.ValueArgument(data=value)

    @staticmethod
    def from_protobuf(protobuf_value: pipeline_pb2.ValueArgument) -> typing.Any:
        # making assumption that the Value message 'data' has 'raw'
        # TODO: add functionality for when Value message has 'error', 'dataset_uri', or 'csv_uri'
        return ValueRaw.from_protobuf(protobuf_value.data.raw)
