from wrapper.pipeline_description import PipelineDescription
import generated_grpc.core_pb2 as core
from wrapper.problem_description import ProblemDescription
import ta2_server

class SearchSolutionsRequest:
    
    def __init__(self, req: core.SearchSolutionsRequest):
        self.protobuf_search_solutions_request = req
        self.user_agent: str = None
        self.version: str = None
        self.time_bound: int = None
        self.priority: int = None
        self.allowed_value_types = None 
        self.pipeline_description: PipelineDescription = None
        self.problem_description: ProblemDescription = None
        self.inputs = None
    
    @staticmethod
    def get_from_protobuf(protobuf_search_solutions_request: core.SearchSolutionsRequest):
        search_solutions_request = SearchSolutionsRequest(protobuf_search_solutions_request)
        pipeline_description_protobuf = search_solutions_request.protobuf_search_solutions_request.template
        search_solutions_request.pipeline_description = PipelineDescription.get_pipeline_from_protobuf_pipeline(pipeline_description_protobuf)
        problem = protobuf_search_solutions_request.problem
        search_solutions_request.problem_description = ProblemDescription.get_from_protobuf(problem)
        search_solutions_request.user_agent = protobuf_search_solutions_request.user_agent
        search_solutions_request.version = protobuf_search_solutions_request.version
        search_solutions_request.time_bound = protobuf_search_solutions_request.time_bound
        search_solutions_request.priority = protobuf_search_solutions_request.priority
        search_solutions_request.allowed_value_types = ta2_server.ALLOWED_VALUE_TYPES
        # TODO: Implement inputs
        
        return search_solutions_request
        
        
    
