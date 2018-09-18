from wrapper.pipeline_description import PipelineDescription
import generated_grpc.core_pb2 as core

class SearchSolutionsRequest:
    
    def __init__(self, req: core.SearchSolutionsRequest):
        self.protobuf_search_solutions_request = req
    
    @staticmethod
    def get_from_protobuf(req: core.SearchSolutionsRequest):
        search_solutions_request = SearchSolutionsRequest(req)
        pipeline_description_protobuf = search_solutions_request.protobuf_search_solutions_request.template
        search_solutions_request.pipeline_description = PipelineDescription.get_pipeline_from_protobuf_pipeline(pipeline_description_protobuf)
        return search_solutions_request
        
        
    
