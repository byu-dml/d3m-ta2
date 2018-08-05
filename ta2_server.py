from concurrent import futures
import time
import uuid
import grpc

import core_pb2
import core_pb2_grpc
from search_process import SearchProcess

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class CoreSession(core_pb2_grpc.CoreServicer):

    def __init__(self):
        self.protocol_version = core_pb2.DESCRIPTOR.GetOptions().Extensions[core_pb2.protocol_version]
        self.search_processes = {}

    def SearchSolutions(self, request, context):
        if request.version != self.protocol_version:
            raise ValueError('TA3 protocol version does not match TA2 protocol version')
        search_id = str(uuid.uuid4())
        self.search_processes[search_id] = SearchProcess(search_id, request)
        return core_pb2.SearchSolutionsResponse(search_id=search_id)

    def GetSearchSolutionsResults(self, request, context):
        if request.search_id not in self.search_processes:
            raise ValueError('search_id provided in GetSearchSolutionsResultsRequest does not match any search_process')
        else:
            return core_pb2.GetSearchSolutionsResultsResponse(progress=None)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    core_pb2_grpc.add_CoreServicer_to_server(CoreSession(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()