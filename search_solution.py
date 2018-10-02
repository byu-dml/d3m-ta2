from generated_grpc import core_pb2
from wrapper.progress import Progress
from d3m.metadata import pipeline as pipeline_module
import uuid


class SearchSolution:

    def __init__(self):
        self.progress: Progress = Progress()
        self.done_ticks: int = 0
        self.id_: str = str(uuid.uuid4())
        self.all_ticks: int = 0
        self.pipeline: pipeline_module.Pipeline = None

        # Optional
        self.internal_score = None
        self.scores = []

    def start_running(self) -> None:
        self.progress.start_running()

    def complete(self, pipeline) -> None:
        self.pipeline = pipeline
        self.progress.complete()

    def get_search_solutions_result(self) -> core_pb2.GetSearchSolutionsResultsResponse:
        return core_pb2.GetSearchSolutionsResultsResponse(progress=self.progress.get_protobuf(),
                                                          done_ticks=self.done_ticks,
                                                          all_ticks=self.all_ticks,
                                                          solution_id=self.id_
                                                          )

    # def get_describe_solution_response(self) -> core_pb2.DescribeSolutionResponse:
    #     return core_pb2.DescribeSolutionResponse(
    #         pipeline=self.pipeline
    #     )
