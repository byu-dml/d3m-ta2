import datetime
from google.protobuf.timestamp_pb2 import Timestamp


class TimestampUtil:

    @staticmethod
    def get_proto_timestamp(created_datetime: datetime.datetime) -> Timestamp:
        created_datetime = created_datetime.replace(tzinfo=None)
        created: Timestamp = Timestamp()
        created.FromDatetime(created_datetime)
        return created

    @staticmethod
    def from_proto_timestamp(created: Timestamp) -> datetime.datetime:
        return created.ToDatetime()

    @staticmethod
    def get_current_proto_timestamp() -> Timestamp:
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        return timestamp

    @staticmethod
    def from_string(string) -> Timestamp:
        timestamp = Timestamp()
        timestamp.FromJsonString(string)
        return timestamp
