import datetime
from google.protobuf.timestamp_pb2 import Timestamp as ProtoTimestamp


class TimestampUtil:

    @staticmethod
    def get_proto_timestamp(created_datetime: datetime.datetime) -> ProtoTimestamp:
        created_datetime = created_datetime.replace(tzinfo=None)
        created: ProtoTimestamp = ProtoTimestamp()
        created.FromDatetime(created_datetime)
        return created

    @staticmethod
    def get_current_proto_timestamp() -> ProtoTimestamp:
        return ProtoTimestamp()
