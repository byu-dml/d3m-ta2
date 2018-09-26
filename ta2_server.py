from concurrent import futures
import time
import uuid
import grpc
import constants
import typing
import d3m.index as index
import d3m.primitive_interfaces.base as base
import sys
import logging
import queue

from generated_grpc import core_pb2_grpc, core_pb2, pipeline_pb2
from search_process import SearchProcess
from config import Config
import wrapper.search_solutions_request as search_solutions_wrapper
from search_worker import SearchWorker
from search_solution import SearchSolution
from wrapper.primitive import Primitive

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_TA2_VERSION = '1.0'
_USER_AGENT = f'BYU TA2 version: {_TA2_VERSION}'
_NUM_SERVER_THREADS = 10
_NUM_WORKER_THREADS = 5


class CoreSession(core_pb2_grpc.CoreServicer):

    def __init__(self, num_workers=_NUM_WORKER_THREADS):
        self.protocol_version = core_pb2.DESCRIPTOR.GetOptions().Extensions[core_pb2.protocol_version]
        self.search_processes: typing.Dict[str, SearchProcess] = {}
        self.work_queue = queue.PriorityQueue()
        self.search_workers: typing.List[SearchWorker] = []

        for i in range(num_workers):
            worker_thread = SearchWorker(search_queue=self.work_queue,
                                         search_processes=self.search_processes,
                                         name=f'worker {i}')
            self.search_workers.append(worker_thread)
            worker_thread.start()

    def stop_workers(self) -> None:
        logging.debug("Stopping workers")
        for worker in self.search_workers:
            worker.interrupt()
        for worker in self.search_workers:
            worker.join()
        logging.debug("Stopped all workers")

    def remove_search_process(self, search_id: str) -> None:
        self.stop_workers_search(search_id)
        if search_id in self.search_processes:
            self.search_processes[search_id].should_stop = True
            del self.search_processes[search_id]

    def stop_workers_search(self, search_id) -> None:
        if search_id in self.search_processes:
            self.search_processes[search_id].should_stop = True

    def stop_search(self, search_id: str) -> None:
        self.stop_workers_search(search_id)
        if search_id in self.search_processes:
            self.search_processes[search_id].should_stop = True

    def add_search_process(self, search_process: SearchProcess) -> None:
        logging.info(f'Inserting {search_process.search_id} into queue and search_processes')
        self.work_queue.put(search_process)
        self.search_processes[search_process.search_id] = search_process

    def find_search_solution(self, solution_id: str) -> typing.Optional[SearchSolution]:
        for search_id, search_process in self.search_processes.items():
            if solution_id in search_process.solutions:
                return search_process.solutions[solution_id]

        return None

    def SearchSolutions(self, request: core_pb2.SearchSolutionsRequest, context) -> core_pb2.SearchSolutionsResponse:
        logging.debug(f'Received SearchSolutionsRequest:\n{request}')
        if request.version != self.protocol_version:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, constants.PROTOCOL_ERROR_MESSAGE)

        problem = request.problem.problem
        if not hasattr(problem, 'id') or problem.id == '':
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "no problem specified")
        search_solutions_request = search_solutions_wrapper.SearchSolutionsRequest.get_from_protobuf(request)
        search_id = str(uuid.uuid4())
        search_process = SearchProcess(search_id, search_solutions_request)
        self.search_processes[search_id] = search_process
        self.add_search_process(search_process)
        return core_pb2.SearchSolutionsResponse(search_id=search_id)

    def GetSearchSolutionsResults(self, request: core_pb2.GetSearchSolutionsResultsRequest, context) -> core_pb2.GetSearchSolutionsResultsResponse:
        logging.debug(f'Received GetSearchSolutionsRequest:\n{request}')
        search_id = request.search_id
        if search_id not in self.search_processes:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, constants.SEARCH_ID_ERROR_MESSAGE)
        else:
            search_process = self.search_processes[search_id]
            sent_solutions: typing.List[str] = []
            for solution in search_process.solutions.values():
                yield solution.get_protobuf_search_solution()
                solution_id = solution.id_
                sent_solutions.append(solution_id)
                logging.debug(f'Sent solution {solution_id}')
            while not search_process.completed:
                time.sleep(1)
                for solution in search_process.solutions.values():
                    if solution.id_ not in sent_solutions:
                        yield solution.get_protobuf_search_solution()
                        solution_id = solution.id_
                        sent_solutions.append(solution_id)
                        logging.debug(f'Sent solution {solution_id}')

    def EndSearchSolutions(self, request: core_pb2.EndSearchSolutionsRequest, context) -> core_pb2.EndSearchSolutionsResponse:
        self.end_search_solutions(request, context)
        return core_pb2.EndSearchSolutionsResponse()

    def end_search_solutions(self, request: core_pb2.EndSearchSolutionsRequest, context) -> None:
        logging.debug(f'Received EndSearchSolutionsRequest:\n{request}')
        search_id: str = request.search_id
        if search_id not in self.search_processes:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, constants.END_SEARCH_SOLUTIONS_ERROR_MESSAGE)
        self.remove_search_process(search_id)

    def StopSearchSolutions(self, request: core_pb2.StopSearchSolutionsRequest, context) -> core_pb2.StopSearchSolutionsResponse:
        logging.debug(f'Received StopSearchSolutionsRequest:\n{request}')
        search_id = request.search_id
        if search_id not in self.search_processes:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, constants.STOP_SEARCH_SOLUTIONS_ERROR_MESSAGE)
        self.stop_search(search_id)

        return core_pb2.StopSearchSolutionsResponse()

    def DescribeSolution(self, request: core_pb2.DescribeSolutionRequest, context) -> core_pb2.DescribeSolutionResponse:
        logging.debug(f'Received DescribeSolutionRequest:\n{request}')
        solution_id = request.solution_id
        search_solution = self.find_search_solution(solution_id)

        if search_solution is None:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, constants.DESCRIBE_SOLUTION_ERROR_MESSAGE)
        return core_pb2.DescribeSolutionResponse()

    def ScoreSolution(self, request: core_pb2.ScoreSolutionRequest, context) -> core_pb2.ScoreSolutionResponse:
        logging.debug(f'Received ScoreSolutionRequest:\n{request}')
        solution_id = request.solution_id
        search_solution = self.find_search_solution(solution_id)
        if search_solution is None:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, constants.SCORE_SOLUTION_ERROR_MESSAGE)

        return core_pb2.ScoreSolutionResponse()

    def GetScoreSolutionResults(self, request, context):
        logging.debug(f'Received GetScoreSolutionResultsRequest:\n{request}')
        yield core_pb2.GetScoreSolutionResultsResponse()

    def FitSolution(self, request, context):
        logging.debug(f'Received FitSolutionRequest:\n{request}')
        return core_pb2.FitSolutionResponse()

    def GetFitSolutionResults(self, request, context):
        logging.debug(f'Received GetFitSolutionResultsRequest:\n{request}')
        yield core_pb2.GetFitSolutionResultsResponse()

    def ProduceSolution(self, request, context):
        logging.debug(f'Received ProduceSolutionRequest:\n{request}')
        return core_pb2.ProduceSolutionResponse()

    def GetProduceSolutionResults(self, request, context):
        logging.debug(f'Received GetProduceSolutionResultsRequest:\n{request}')
        yield core_pb2.GetProduceSolutionResultsResponse

    def SolutionExport(self, request, context):
        logging.debug(f'Received SolutionExportRequest:\n{request}')
        return core_pb2.SolutionExportResponse()

    def UpdateProblem(self, request, context):
        logging.debug(f'Received UpdateProblemRequest:\n{request}')
        return core_pb2.UpdateProblemRequest()

    def ListPrimitives(self, request: core_pb2.ListPrimitivesRequest, context) -> core_pb2.ListPrimitivesResponse:
        logging.debug(f'Received ListPrimitivesRequest:\n{request}')
        primitive_bases: typing.List[base.PrimitiveBase] = index.get_loaded_primitives()
        primitives: typing.List[pipeline_pb2.primitive__pb2.Primitive] = []

        if len(primitive_bases) == 0:
            index.load_all()
            primitive_bases = index.get_loaded_primitives()
        for primitive_base in primitive_bases:
            metadata = primitive_base.metadata.to_json_structure()
            primitive = Primitive.get_primitive_from_json(metadata)
            primitives.append(primitive)

        return core_pb2.ListPrimitivesResponse(primitives=primitives)

    def Hello(self, request: core_pb2.HelloRequest, context):
        logging.debug(f'Received HelloRequest:\n{request}')
        return core_pb2.HelloResponse(version=_TA2_VERSION,
                                      user_agent=_USER_AGENT,
                                      allowed_value_types=constants.ALLOWED_VALUE_TYPES,
                                      supported_extensions=[]
                                      )


def serve():
    initialize_logging()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_NUM_SERVER_THREADS))
    core_session = CoreSession()
    core_pb2_grpc.add_CoreServicer_to_server(core_session, server)
    server.add_insecure_port('[::]:' + Config.server_port)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        core_session.stop_workers()
        server.stop(0)


def initialize_logging():
    root = logging.getLogger()
    root.setLevel(Config.log_level)
    formatter = logging.Formatter('%(asctime)s - thread %(threadName)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    root.addHandler(ch)


if __name__ == '__main__':
    serve()
