from factory.pipeline_description_factory import PipelineDescriptionFactory
import generated_grpc.core_pb2 as core
from wrapper.problem.problem_description import ProblemDescription
import constants
from d3m.metadata import pipeline as pipeline_module


class SearchSolutionsRequest:

    def __init__(self, req: core.SearchSolutionsRequest):
        self.protobuf_search_solutions_request = req
        self.user_agent: str = None
        self.version: str = None
        self.time_bound: int = None
        self.priority: int = None
        self.allowed_value_types = None
        self.pipeline: pipeline_module.Pipeline = None
        self.problem_description: ProblemDescription = None
        self.inputs = None

    @staticmethod
    def get_from_protobuf(protobuf_search_solutions_request: core.SearchSolutionsRequest):
        search_solutions_request = SearchSolutionsRequest(protobuf_search_solutions_request)
        template = protobuf_search_solutions_request.template
        has_template = template is not None and len(template.steps) > 0

        if has_template:
            pipeline_description_protobuf = search_solutions_request.protobuf_search_solutions_request.template
            search_solutions_request.pipeline = PipelineDescriptionFactory.from_protobuf_pipeline_description(
                pipeline_description_protobuf)
        problem = protobuf_search_solutions_request.problem
        search_solutions_request.problem_description = ProblemDescription.get_from_protobuf(problem)
        search_solutions_request.user_agent = protobuf_search_solutions_request.user_agent
        search_solutions_request.version = protobuf_search_solutions_request.version
        search_solutions_request.time_bound = protobuf_search_solutions_request.time_bound
        search_solutions_request.priority = protobuf_search_solutions_request.priority
        search_solutions_request.allowed_value_types = constants.ALLOWED_VALUE_TYPES
        # TODO: Add validation of inputs for pipelines
        # Note: inputs are optional for fully specified pipelines with all hyper-parameters fixed
        search_solutions_request.inputs = protobuf_search_solutions_request.inputs

        return search_solutions_request

    def is_pipeline_fully_specified(self) -> bool:
        if self.pipeline is None:
            return False
        has_no_free_hyperparams = sum([len(free) for free in self.pipeline.get_free_hyperparams()]) == 0
        has_no_placeholders = not self.pipeline.has_placeholder()
        return has_no_free_hyperparams and has_no_placeholders






