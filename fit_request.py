from d3m.runtime import Runtime

class FitRequest():

    def __init__(self, request_id, pipeline):
        self.request_id = request_id
        self.runtime = Runtime(pipeline=pipeline)

    def fit(self):
        result = self.runtime.fit(inputs=[dataset_input])