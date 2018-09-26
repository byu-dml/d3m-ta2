import pytest
import grpc
import generated_grpc.problem_pb2 as grpc_problem
from generated_grpc import core_pb2_grpc, core_pb2
from d3m import runtime
from d3m.metadata import pipeline as pipeline_module
from config import Config
from wrapper.problem_description import ProblemDescription
import ta2_server


@pytest.fixture(scope='module')
def grpc_channel() -> grpc.Channel:
    return grpc.insecure_channel(Config.server_host + ':' + Config.server_port)


@pytest.fixture(scope='module')
def stub(grpc_channel: grpc.Channel) -> core_pb2_grpc.CoreStub:
    return core_pb2_grpc.CoreStub(grpc_channel)


@pytest.fixture(scope='module')
def protocol_version() -> str:
    return core_pb2.DESCRIPTOR.GetOptions().Extensions[core_pb2.protocol_version]


@pytest.fixture()
def random_forest_pipeline() -> pipeline_module.Pipeline:
    pipeline_path = 'test/pipelines/random_forest_classification.yml'
    return runtime.get_pipeline(pipeline_path)


@pytest.fixture()
def sick_problem() -> grpc_problem.ProblemDescription:
    return ProblemDescription.problem_json_to_protobuf(
        '/datasets/seed_datasets_current/38_sick/38_sick_problem/problemDoc.json')


@pytest.fixture()
def no_worker_core_session() -> ta2_server.CoreSession:
    return ta2_server.CoreSession(0)
