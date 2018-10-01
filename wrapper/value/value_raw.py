from generated_grpc import value_pb2
import typing


class ValueRaw:
    def __init__(self, raw):
        self.raw = raw

    def to_protobuf(self) -> value_pb2.ValueRaw:
        value_raw = None
        if self.raw == value_pb2.NULL_VALUE:
            value_raw = value_pb2.ValueRaw(null=self.raw)
        elif isinstance(self.raw, bool):
            value_raw = value_pb2.ValueRaw(bool=self.raw)
        elif isinstance(self.raw, float):
            value_raw = value_pb2.ValueRaw(double=self.raw)
        elif isinstance(self.raw, int):
            value_raw = value_pb2.ValueRaw(int64=self.raw)
        elif isinstance(self.raw, str):
            value_raw = value_pb2.ValueRaw(string=self.raw)
        elif isinstance(self.raw, bytes):
            value_raw = value_pb2.ValueRaw(bytes=self.raw)
        elif isinstance(self.raw, list):
            value_list: typing.List[value_pb2.ValueRaw] = [temp_raw.to_protobuf() for temp_raw in self.raw]
            value_raw = value_pb2.ValueRaw(list=value_list)
        elif isinstance(self.raw, dict):
            value_dict: typing.Dict[str, value_pb2.ValueRaw] = {}
            for key, value in self.raw.items():
                value_dict[key] = value.to_protobuf()
            value_raw = value_pb2.ValueRaw(dict=value_dict)

        return value_raw
