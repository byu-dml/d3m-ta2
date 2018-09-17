from generated_grpc import pipeline_pb2


class Primitive:

    @staticmethod
    def get_primitive_from_description(primitive_description: dict) -> pipeline_pb2.primitive__pb2.Primitive:
        id_ = primitive_description['id']
        version = primitive_description['version']
        python_path = primitive_description['python_path']
        name = primitive_description['name']
        digest = None
        if 'digest' in primitive_description:
            digest = primitive_description['digest']

        primitive = pipeline_pb2.primitive__pb2.Primitive(id=id_, version=version, python_path=python_path, name=name, digest=digest)
        return primitive
