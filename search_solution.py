from wrapper.progress import Progress
import uuid


class SearchSolution:

    def __init__(self):
        self.progress: Progress = Progress()
        self.done_ticks: int = None
        self.id_: uuid = uuid.uuid4()

        # Optional
        self.internal_score = None
        self.scores = []

    def start_running(self) -> None:
        self.progress.start_running()

    def complete(self) -> None:
        self.progress.complete()
