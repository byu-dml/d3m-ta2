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

    def get_protobuf(self):
        return core_pb2.Progress(state=self.state,
                                 status=self.status,
                                 start=self.start,
                                 end=self.end
                                 )
