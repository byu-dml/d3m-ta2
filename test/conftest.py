import pytest
import grpc
import generated_grpc.problem_pb2 as grpc_problem
from generated_grpc import core_pb2_grpc, core_pb2
from d3m import runtime
from d3m.metadata import pipeline as pipeline_module
from config import Config
from wrapper.problem.problem_description import ProblemDescription
import typing
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
def random_forest_pipeline_fully_specified() -> pipeline_module.Pipeline:
    pipeline_path = 'test/pipelines/random_forest_classification.yml'
    pipeline = runtime.get_pipeline(pipeline_path)
    steps: typing.List[pipeline_module.PrimitiveStep] = pipeline.steps

    denormalize_step = steps[0]
    denormalize_step.add_hyperparameter('starting_resource', pipeline_module.ArgumentType.VALUE, "None")
    denormalize_step.add_hyperparameter('recursive', pipeline_module.ArgumentType.VALUE, True)
    denormalize_step.add_hyperparameter('many_to_many', pipeline_module.ArgumentType.VALUE, True)
    denormalize_step.add_hyperparameter('discard_not_joined_tabular_resources', pipeline_module.ArgumentType.VALUE, False)
    assert len(denormalize_step.get_free_hyperparams()) == 0

    dataset_to_dataframe = steps[1]
    dataset_to_dataframe.add_hyperparameter('dataframe_resource', pipeline_module.ArgumentType.VALUE, None)

    column_parser = steps[2]
    parse_types_default = [
        "http://schema.org/Boolean",
        "https://metadata.datadrivendiscovery.org/types/CategoricalData",
        "http://schema.org/Integer",
        "http://schema.org/Float",
        "https://metadata.datadrivendiscovery.org/types/FloatVector",
        "http://schema.org/Time"
    ]
    column_parser.add_hyperparameter('parse_semantic_types', pipeline_module.ArgumentType.VALUE, parse_types_default)
    column_parser.add_hyperparameter('use_columns', pipeline_module.ArgumentType.VALUE, [0])
    column_parser.add_hyperparameter('exclude_columns', pipeline_module.ArgumentType.VALUE, [1])
    column_parser.add_hyperparameter('return_result', pipeline_module.ArgumentType.VALUE, 'replace')
    column_parser.add_hyperparameter('add_index_columns', pipeline_module.ArgumentType.VALUE, True)
    column_parser.add_hyperparameter('parse_categorical_target_columns', pipeline_module.ArgumentType.VALUE, False)

    imputer = steps[3]
    imputer.add_hyperparameter('missing_values', pipeline_module.ArgumentType.VALUE, "NaN")
    imputer.add_hyperparameter('strategy', pipeline_module.ArgumentType.VALUE, "mean")
    imputer.add_hyperparameter('axis', pipeline_module.ArgumentType.VALUE, 0)
    imputer.add_hyperparameter('use_columns', pipeline_module.ArgumentType.VALUE, [0])
    imputer .add_hyperparameter('exclude_columns', pipeline_module.ArgumentType.VALUE, [1])
    imputer.add_hyperparameter('copy', pipeline_module.ArgumentType.VALUE, True)
    imputer.add_hyperparameter('return_result', pipeline_module.ArgumentType.VALUE, 'replace')
    imputer.add_hyperparameter('add_index_columns', pipeline_module.ArgumentType.VALUE, True)

    random_forest = steps[4]
    random_forest.add_hyperparameter('n_estimators', pipeline_module.ArgumentType.VALUE, 10)
    random_forest.add_hyperparameter('criterion', pipeline_module.ArgumentType.VALUE, 'gini')
    random_forest.add_hyperparameter('max_features', pipeline_module.ArgumentType.VALUE, 'auto')
    random_forest.add_hyperparameter('max_depth', pipeline_module.ArgumentType.VALUE, 100)
    random_forest.add_hyperparameter('min_samples_split', pipeline_module.ArgumentType.VALUE, 2)
    random_forest.add_hyperparameter('min_samples_leaf', pipeline_module.ArgumentType.VALUE, 1)
    random_forest.add_hyperparameter('min_weight_fraction_leaf', pipeline_module.ArgumentType.VALUE, float(0))
    random_forest.add_hyperparameter('max_leaf_nodes', pipeline_module.ArgumentType.VALUE, 10000)
    random_forest.add_hyperparameter('min_impurity_decrease', pipeline_module.ArgumentType.VALUE, float(10))
    random_forest.add_hyperparameter('bootstrap', pipeline_module.ArgumentType.VALUE, True)
    random_forest.add_hyperparameter('oob_score', pipeline_module.ArgumentType.VALUE, False)
    random_forest.add_hyperparameter('n_jobs', pipeline_module.ArgumentType.VALUE, 1)
    random_forest.add_hyperparameter('use_columns', pipeline_module.ArgumentType.VALUE, [0])
    random_forest.add_hyperparameter('exclude_columns', pipeline_module.ArgumentType.VALUE, [1])
    random_forest.add_hyperparameter('return_result', pipeline_module.ArgumentType.VALUE, 'append')
    random_forest.add_hyperparameter('add_index_columns', pipeline_module.ArgumentType.VALUE, True)

    construct_predictions = steps[5]
    construct_predictions.add_hyperparameter('use_columns', pipeline_module.ArgumentType.VALUE, [0])
    construct_predictions .add_hyperparameter('exclude_columns', pipeline_module.ArgumentType.VALUE, [1])

    assert sum([len(free) for free in pipeline.get_free_hyperparams()]) == 0, 'There are some free hyperparameters'

    return pipeline


@pytest.fixture()
def sick_problem() -> grpc_problem.ProblemDescription:
    return ProblemDescription.problem_json_to_protobuf(
        '/datasets/seed_datasets_current/38_sick/38_sick_problem/problemDoc.json')


@pytest.fixture()
def no_worker_core_session() -> ta2_server.CoreSession:
    return ta2_server.CoreSession(0)


@pytest.fixture()
def search_id(stub: core_pb2_grpc.CoreStub, protocol_version: str, sick_problem: grpc_problem.ProblemDescription) -> str:
    request = core_pb2.SearchSolutionsRequest(version=protocol_version, problem=sick_problem)
    response: core_pb2.SearchSolutionsResponse = stub.SearchSolutions(request)
    return response.search_id

@pytest.fixture()
def fully_specified_search_id(stub: core_pb2_grpc.CoreStub, protocol_version: str, random_forest_pipeline_fully_specified: pipeline_module.Pipeline, sick_problem: grpc_problem.ProblemDescription) -> str:
    request = core_pb2.SearchSolutionsRequest(version=protocol_version, problem=sick_problem)
    response: core_pb2.SearchSolutionsResponse = stub.SearchSolutions(request)
    search_id = response.search_id
    request = core_pb2.GetSearchSolutionsResultsRequest(search_id=search_id)
    response: core_pb2.GetSearchSolutionsResultsResponse = stub.GetSearchSolutionsResults(request)
    for result in response:
        return result.solution_id

