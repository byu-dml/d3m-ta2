from generated_grpc import primitive_pb2
import typing


class Primitive:

    def __init__(self, primitive_description: typing.Dict):
        self.id_ = primitive_description['id']
        self.version = primitive_description['version']
        self.python_path = primitive_description['python_path']
        self.name = primitive_description['name']
        self.digest = None
        if 'digest' in primitive_description:
            self.digest = primitive_description['digest']

    def to_protobuf(self) -> primitive_pb2.Primitive:
        primitive = primitive_pb2.Primitive(id=self.id_,
                                            version=self.version,
                                            python_path=self.python_path,
                                            name=self.name,
                                            digest=self.digest
                                            )
        return primitive

    @staticmethod
    def from_protobuf(protobuf_primitive: primitive_pb2.Primitive) -> typing.Dict:
        primitive_description = {}
        primitive_description['id'] = protobuf_primitive.id
        primitive_description['version'] = protobuf_primitive.version
        primitive_description['python_path'] = protobuf_primitive.python_path
        primitive_description['name'] = protobuf_primitive.name
        primitive_description['digest'] = protobuf_primitive.digest
        return primitive_description

