from generated_grpc import core_pb2
from wrapper.core.progress import Progress
from d3m.metadata import pipeline as pipeline_module
from d3m.runtime import Runtime
from d3m.container.dataset import Dataset, D3MDatasetLoader
from fit_request import FitRequest
import uuid


class SearchSolution:

    def __init__(self):
        self.progress: Progress = Progress()
        self.done_ticks: int = 0
        self.id_: str = str(uuid.uuid4())
        self.all_ticks: int = 0
        self.pipeline: pipeline_module.Pipeline = None
        self.fit_requests = []
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

    def fit(self, inputs, request_id):
        grpc_inputs = inputs[0]
        dataset_uri = grpc_inputs.dataset_uri  # inputs is string which is a URI to the datasetDoc.json
        dataset_input = D3MDatasetLoader().load(dataset_uri)
        runtime = Runtime(pipeline=self.pipeline)
        result = runtime.fit(inputs=[dataset_input])
        fit_request = FitRequest(request_id, self.pipeline)
        self.fit_requests.append(fit_request)

    # def get_describe_solution_response(self) -> core_pb2.DescribeSolutionResponse:
    #     return core_pb2.DescribeSolutionResponse(
    #         pipeline=self.pipeline
    #     )
