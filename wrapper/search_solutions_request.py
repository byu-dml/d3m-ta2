from wrapper.pipeline_description import PipelineDescription
import generated_grpc.core_pb2 as core

class SearchSolutionsRequest:
    
    def __init__(self, req: core.SearchSolutionsRequest):
        self.protobuf_search_solutions_request = req
    
    @staticmethod
    def get_from_protobuf(req: core.SearchSolutionsRequest):
        pipeline_description_protobuf = req.pipeline_description
        search_solutions_request = SearchSolutionsRequest(req)
        search_solutions_request.pipeline_description = PipelineDescription.get_from_protobuf(pipeline_description_protobuf)
        
        return search_solutions_request
        
        
    
