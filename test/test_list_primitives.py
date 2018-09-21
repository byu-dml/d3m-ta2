import pytest
from generated_grpc import core_pb2, core_pb2_grpc
from pprint import pprint


class TestListPrimitives:

    @staticmethod
    def test_is_list_primitives_response(stub: core_pb2_grpc.CoreStub):
        response = None
        try:
            response = stub.ListPrimitives(core_pb2.ListPrimitivesRequest())
        except Exception as e:
            pytest.fail(f'call to ListPrimitives failed to return a valid response with exception {str(e)}')

        assert isinstance(response, core_pb2.ListPrimitivesResponse), 'call to ListPrimitives did not return an instance of SearchSolutionsResponse'

    @staticmethod
    def test_is_list_primitives_response_contains_required_fields(stub: core_pb2_grpc.CoreStub):
        response = stub.ListPrimitives(core_pb2.ListPrimitivesRequest())
        primitives = response.primitives
        for primitive in primitives:
            assert primitive.id is not None, 'Primitive did not contain an id'
            assert primitive.version is not None, 'Primitive did not contain a version'
            assert primitive.python_path is not None, 'Primitive did not contain a python_path'
            assert primitive.name is not None, 'Primitive did not contain a name'

        assert primitives is not None and len(primitives) > 0, 'No primitives were returned'

