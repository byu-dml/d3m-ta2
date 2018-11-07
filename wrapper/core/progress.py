from util.timestamp_util import TimestampUtil
from generated_grpc import core_pb2


UNKNOWN = 0
PENDING = 1
RUNNING = 2
COMPLETED = 3
ERRORED = 4


class Progress:

    def __init__(self):
        self.state: int = PENDING
        self.status = None
        self.start = None
        self.end = None

    def complete(self):
        self.state = COMPLETED
        self.end = TimestampUtil.get_current_proto_timestamp()

    def start_running(self):
        self.state = RUNNING
        self.start = TimestampUtil.get_current_proto_timestamp()

    def to_json_structure(self) -> dict:
        json_structure = {
            'state': self.state,
            'status': self.status,
            'start': None,
            'end': None
        }
        if self.start is not None:
            json_structure['start'] = self.start.ToJsonString()
        if self.end is not None:
            json_structure['end'] = self.end.ToJsonString()
        return json_structure

    @staticmethod
    def from_json_structure(json_structure: dict) -> 'Progress':
        progress = Progress()
        progress.state = json_structure['state']
        progress.status = json_structure['status']
        start = json_structure['start']
        if start is not None:
            start = TimestampUtil.from_string(start)
        progress.start = start
        end = json_structure['end']
        if end is not None:
            end = TimestampUtil.from_string(end)
        progress.end = end

        return progress

    def get_protobuf(self):
        return core_pb2.Progress(state=self.state,
                                 status=self.status,
                                 start=self.start,
                                 end=self.end
                                 )
