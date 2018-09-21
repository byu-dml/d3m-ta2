from concurrent import futures
import time
import uuid
import grpc
import constants
import typing
import d3m.index as index
import d3m.primitive_interfaces.base as base

from generated_grpc import core_pb2_grpc, core_pb2
from search_process import SearchProcess
from config import Config
import wrapper.search_solutions_request as search_solutions_wrapper

from wrapper.primitive import Primitive

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_ALLOWED_VALUE_TYPES = ['RAW', 'DATASET_URI', 'CSV_URI']
_TA2_VERSION = '1.0'
_USER_AGENT = f'BYU TA2 version: {_TA2_VERSION}'
_NUM_SERVER_THREADS = 10


class CoreSession(core_pb2_grpc.CoreServicer):

    def __init__(self):
        self.protocol_version = core_pb2.DESCRIPTOR.GetOptions().Extensions[core_pb2.protocol_version]
        self.search_processes: typing.Dict[str, SearchProcess] = {}

    def SearchSolutions(self, request: core_pb2.SearchSolutionsRequest, context) -> core_pb2.SearchSolutionsResponse:
        if request.version != self.protocol_version:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, constants.PROTOCOL_ERROR_MESSAGE)

        problem = request.problem.problem
        if not hasattr(problem, 'id') or problem.id == '':
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "no problem specified")
        search_solutions_request = search_solutions_wrapper.SearchSolutionsRequest.get_from_protobuf(request)
        search_id = str(uuid.uuid4())
        self.search_processes[search_id] = SearchProcess(search_id, search_solutions_request)
        return core_pb2.SearchSolutionsResponse(search_id=search_id)

    def GetSearchSolutionsResults(self, request, context):
        if request.search_id not in self.search_processes:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, constants.SEARCH_ID_ERROR_MESSAGE)
        else:
            # responses = self.search_processes[request.search_id].GetSearchSolutionsResults()
            # for response in responses:
            #     yield response
            yield core_pb2.GetSearchSolutionsResultsResponse(progress=None)
            yield core_pb2.GetSearchSolutionsResultsResponse(progress=None)

    def EndSearchSolutions(self, request, context):
        if request.search_id not in self.search_processes:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, constants.END_SEARCH_SOLUTIONS_ERROR_MESSAGE)
        return core_pb2.EndSearchSolutionsResponse()

    def StopSearchSolutions(self, request, context):
        if request.search_id not in self.search_processes:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, constants.STOP_SEARCH_SOLUTIONS_ERROR_MESSAGE)
        return core_pb2.StopSearchSolutionsResponse()

    def DescribeSolution(self, request, context):
        if request.solution_id not in self.solutions:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, constants.DESCRIBE_SOLUTION_ERROR_MESSAGE)
        return core_pb2.DescribeSolutionResponse()

    def ScoreSolution(self, request, context):
        if request.solution_id not in self.solutions:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, constants.SCORE_SOLUTION_ERROR_MESSAGE)
        return core_pb2.ScoreSolutionResponse()

    def GetScoreSolutionResults(self, request, context):
        yield core_pb2.GetScoreSolutionResultsResponse()

    def FitSolution(self, request, context):
        return core_pb2.FitSolutionResponse()

    def GetFitSolutionResults(self, request, context):
        yield core_pb2.GetFitSolutionResultsResponse()

    def ProduceSolution(self, request, context):
        return core_pb2.ProduceSolutionResponse()

    def GetProduceSolutionResults(self, request, context):
        yield core_pb2.GetProduceSolutionResultsResponse

    def SolutionExport(self, request, context):
        return core_pb2.SolutionExportResponse()

    def UpdateProblem(self, request, context):
        return core_pb2.UpdateProblemRequest()

    def ListPrimitives(self, request, context):
        primitive_bases: typing.List[base.PrimitiveBase] = index.get_loaded_primitives()
        primitives = []
        
        if len(primitive_bases) == 0:
            index.load_all()
            primitive_bases = index.get_loaded_primitives()
        for primitive_base in primitive_bases:
            metadata = primitive_base.metadata.to_json_structure()
            primitive = Primitive.get_primitive_from_json(metadata)
            primitives.append(primitive)
                
        return core_pb2.ListPrimitivesResponse(primitives=primitives)

    def Hello(self, request, context):
        return core_pb2.HelloResponse(version=_TA2_VERSION,
                                      user_agent=_USER_AGENT,
                                      allowed_value_types=_ALLOWED_VALUE_TYPES,
                                      supported_extensions=[]
                                      )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_NUM_SERVER_THREADS))
    core_pb2_grpc.add_CoreServicer_to_server(CoreSession(), server)
    server.add_insecure_port('[::]:' + Config.server_port)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
