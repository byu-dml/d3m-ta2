import generated_grpc.problem_pb2 as grpc_problem
from wrapper.problem.problem_performance_metric import ProblemPerformanceMetric


# from d3m.metadata.problem import TaskSubtype, TaskType

class Problem:

    def __init__(self, protobuf_problem: grpc_problem.Problem):
        self.grpc_problem = protobuf_problem
        self.id = None
        self.version = None
        self.name = None
        self.description = None

    @staticmethod
    def get_from_protobuf(protobuf_problem: grpc_problem.Problem):
        problem = Problem(protobuf_problem)
        problem.id = protobuf_problem.id
        problem.version = protobuf_problem.version
        problem.name = protobuf_problem.name

        task_type: grpc_problem.TaskType = protobuf_problem.task_type
        problem.task_type = grpc_problem.TaskType.Name(task_type)

        task_subtype: grpc_problem.TaskSubtype = protobuf_problem.task_subtype
        problem.task_subtype = grpc_problem.TaskSubtype.Name(task_subtype)

        performance_metrics = [ProblemPerformanceMetric.get_from_protobuf(problem_performance_metric) for
                               problem_performance_metric in protobuf_problem.performance_metrics]
        problem.performance_metrics = performance_metrics

        return problem
