from generated_grpc import core_pb2
from wrapper.progress import Progress
import uuid


class SearchSolution:

    def __init__(self):
        self.progress: Progress = Progress()
        self.done_ticks: int = 0
        self.id_: str = str(uuid.uuid4())
        self.all_ticks: int = 0

        # Optional
        self.internal_score = None
        self.scores = []

    def start_running(self) -> None:
        self.progress.start_running()

    def complete(self) -> None:
        self.progress.complete()

    def get_protobuf_search_solution(self):
        return core_pb2.GetSearchSolutionsResultsResponse(progress=self.progress.get_protobuf(),
                                                          done_ticks=self.done_ticks,
                                                          all_ticks=self.all_ticks,
                                                          solution_id=self.id_
                                                          )
