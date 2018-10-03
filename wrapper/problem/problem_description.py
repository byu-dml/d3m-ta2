import generated_grpc.problem_pb2 as grpc_problem
from wrapper.problem.problem import Problem
from wrapper.problem.problem_input import ProblemInput
from d3m.metadata import problem as problem_module


class ProblemDescription:

    def __init__(self, req: grpc_problem.ProblemDescription):
        self.protobuf_problem_description = req
        self.problem = None
        self.inputs = None

    @staticmethod
    def get_from_protobuf(protobuf_problem_description: grpc_problem.ProblemDescription):
        problem_description = ProblemDescription(protobuf_problem_description)
        problem_description.problem = Problem.get_from_protobuf(protobuf_problem_description.problem)
        problem_description.inputs = [ProblemInput.get_from_protobuf(input) for input in protobuf_problem_description.inputs]

        return problem_description

    @staticmethod
    def problem_json_to_protobuf(path: str) -> grpc_problem.ProblemDescription:
        problem_description = problem_module.parse_problem_description(path)
        del problem_description['schema']
        del problem_description['outputs']

        problem = problem_description['problem']

        task_type: grpc_problem.TaskType = problem['task_type']
        problem['task_type'] = task_type.value

        task_subtype: grpc_problem.TaskSubtype = problem['task_subtype']
        problem['task_subtype'] = task_subtype.value

        new_performance_metrics = ProblemDescription.get_performance_metrics(problem)

        problem['performance_metrics'] = new_performance_metrics
        problem_description['problem'] = problem

        return problem_description

    @staticmethod
    def get_performance_metrics(problem):
        new_performance_metrics = []
        for performance_metric in problem['performance_metrics']:
            proto_performance_metric = {}
            metric = performance_metric['metric'].value
            proto_performance_metric['metric'] = metric
            params = performance_metric['params']
            if 'k' in params:
                proto_performance_metric['k'] = params['k']
            if 'pos_label' in params:
                proto_performance_metric['pos_label'] = params['pos_label']

            new_performance_metrics.append(proto_performance_metric)
        return new_performance_metrics
