from generated_grpc import value_pb2
import typing


class ValueRaw:
    def __init__(self, raw):
        self.raw = raw

    def to_protobuf(self) -> value_pb2.ValueRaw:
        value_raw = None
        if self.raw is None:
            value_raw = value_pb2.ValueRaw(null=value_pb2.NULL_VALUE)
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
            value_list_items: typing.List[value_pb2.ValueRaw] = [temp_raw.to_protobuf() for temp_raw in self.raw]
            value_list: value_pb2.ValueList = value_pb2.ValueList(items=value_list_items)
            value_raw = value_pb2.ValueRaw(list=value_list)
        elif isinstance(self.raw, dict):
            value_dict_items: typing.Dict[str, value_pb2.ValueRaw] = {}
            for key, value in self.raw.items():
                value_dict_items[key] = value.to_protobuf()
            value_dict: value_pb2.ValueDict = value_pb2.ValueDict(items=value_dict_items)
            value_raw = value_pb2.ValueRaw(dict=value_dict)

        return value_raw

    @staticmethod
    def from_protobuf(protobuf_value_raw: value_pb2.ValueRaw) -> typing.Any:
        value_name = protobuf_value_raw.WhichOneof('raw')
        if value_name == 'null':
            value = None
        elif value_name == 'list':
            value = protobuf_value_raw.list.items
        elif value_name == 'dict':
            value = protobuf_value_raw.dict.items
        else:
            value = getattr(protobuf_value_raw, value_name)
        return value
