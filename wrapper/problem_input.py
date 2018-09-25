import generated_grpc.problem_pb2 as grpc_problem
from wrapper.problem_target import ProblemTarget
from pprint import pprint


class ProblemInput:
    
    def __init__(self, protobuf_problem_input: grpc_problem.ProblemInput):
        self.protobuf_problem_input = protobuf_problem_input
        self.dataset_id = None
        
    
    @staticmethod
    def get_from_protobuf(protobuf_problem_input: grpc_problem.ProblemInput):
        problem_input = ProblemInput(protobuf_problem_input)
        problem_input.dataset_id = protobuf_problem_input.dataset_id
        targets = [ProblemTarget.get_from_protobuf(protobuf_problem_target) for protobuf_problem_target in protobuf_problem_input.targets]
        problem_input.targets = targets

        return problem_input

        
        
        