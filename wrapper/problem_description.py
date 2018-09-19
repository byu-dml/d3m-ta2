import generated_grpc.problem_pb2 as grpc_problem
from wrapper.problem import Problem
from wrapper.problem_input import ProblemInput
from pprint import pprint


class ProblemDescription:
    
    def __init__(self, req: grpc_problem.ProblemDescription):
        self.protobuf_problem_description = req
        self.problem = None
        self.inputs = None
        
    @staticmethod
    def get_from_protobuf(protobuf_problem_description: grpc_problem.ProblemDescription):
        problem_description = ProblemDescription(protobuf_problem_description)
        problem_description.problem  = Problem.get_from_protobuf(protobuf_problem_description.problem)
        problem_description.inputs = ProblemInput.get_from_protobuf(protobuf_problem_description.inputs) 
        
        return problem_description
        
