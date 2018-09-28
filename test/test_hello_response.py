import pytest
from generated_grpc import core_pb2, core_pb2_grpc, value_pb2


class TestHelloResponse:

    @staticmethod
    def test_is_hello_response(stub: core_pb2_grpc.CoreStub):
        response = None
        try:
            response = stub.Hello(core_pb2.HelloRequest())
        except Exception as e:
            pytest.fail(f'call to Hello failed to return a valid response with exception {str(e)}')

        assert isinstance(response,
                          core_pb2.HelloResponse), 'call to Hello did not return an instance of SearchSolutionsResponse'

    @staticmethod
    def test_response_contains_required_fields(stub: core_pb2_grpc.CoreStub):
        response = stub.Hello(core_pb2.HelloRequest())

        assert response.version is not None and response.version is not '', 'HelloResponse did not contain a version'
        assert response.user_agent is not None and response.user_agent is not '', 'HelloResponse did not contain user_agent'
        assert response.supported_extensions is not None, 'HelloResponse did not contain supported_extensions'
        allowed_value_types = response.allowed_value_types
        assert allowed_value_types is not None and len(
            allowed_value_types) > 0, 'HelloResponse did not contain allowed_value_types'
        for value_type in allowed_value_types:
            actual_allowed_value_types = value_pb2.ValueType.values()
            assert value_type in actual_allowed_value_types, f'HelloResponse contained an invalid value type. type {value_type} allowed types{actual_allowed_value_types}'
