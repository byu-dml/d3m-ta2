import pytest
import grpc
from generated_grpc import core_pb2_grpc, core_pb2


@pytest.fixture(scope='module')
def grpc_channel() -> grpc.Channel:
    return grpc.insecure_channel('localhost:50052')


@pytest.fixture(scope='module')
def stub(grpc_channel: grpc.Channel) -> core_pb2_grpc.CoreStub:
    return core_pb2_grpc.CoreStub(grpc_channel)


@pytest.fixture(scope='module')
def protocol_version() -> str:
    return core_pb2.DESCRIPTOR.GetOptions().Extensions[core_pb2.protocol_version]