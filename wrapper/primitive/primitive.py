from generated_grpc import pipeline_pb2


class Primitive:

    @staticmethod
    def get_primitive_from_json(json_description: dict) -> pipeline_pb2.primitive__pb2.Primitive:
        id_ = json_description['id']
        version = json_description['version']
        python_path = json_description['python_path']
        name = json_description['name']
        digest = None
        if 'digest' in json_description:
            digest = json_description['digest']

        primitive = pipeline_pb2.primitive__pb2.Primitive(id=id_, version=version, python_path=python_path, name=name, digest=digest)
        return primitive
