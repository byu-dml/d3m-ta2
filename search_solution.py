from generated_grpc import core_pb2
from wrapper.core.progress import Progress
from d3m.metadata import pipeline as pipeline_module
import uuid


class SearchSolution:

    def __init__(self, search_id: str):
        self.progress: Progress = Progress()
        self.done_ticks: int = 0
        self.id_: str = str(uuid.uuid4())
        self.all_ticks: int = 0
        self.pipeline: pipeline_module.Pipeline = None
        self.search_id = search_id
        self.mongo_id = None

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

    def to_json_structure(self) -> dict:
        json_structure = {
            'progress': self.progress.to_json_structure(),
            'done_ticks': self.done_ticks,
            'id': self.id_,
            'all_ticks': self.all_ticks,
            'search_id': self.search_id,
            'pipeline': None,
            'internal_scores': self.internal_score,
            'scores': self.scores
        }
        if self.pipeline is not None:
            json_structure['pipeline'] = self.pipeline.to_json_structure()
        if self.mongo_id is not None:
            json_structure['_id'] = self.mongo_id

        return json_structure

    @staticmethod
    def from_json_structure(json_structure) -> 'SearchSolution':
        search_solution = SearchSolution(json_structure['search_id'])
        search_solution.progress = Progress.from_json_structure(json_structure['progress'])
        search_solution.done_ticks = json_structure['done_ticks']
        search_solution.id_ = json_structure['id']
        search_solution.all_ticks = json_structure['all_ticks']
        pipeline_description = json_structure['pipeline']
        if pipeline_description is not None:
            search_solution.pipeline = pipeline_module.Pipeline.from_json_structure(pipeline_description)
        search_solution.pipeline = pipeline_description
        search_solution.internal_score = json_structure['internal_scores']
        search_solution.scores = json_structure['scores']
        if '_id' in json_structure:
            search_solution.mongo_id = json_structure['_id']

        return search_solution

    # def get_describe_solution_response(self) -> core_pb2.DescribeSolutionResponse:
    #     return core_pb2.DescribeSolutionResponse(
    #         pipeline=self.pipeline
    #     )
