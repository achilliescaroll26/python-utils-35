import collections
import functools

class DataPipeline:
    def __init__(self, processors=None):
        self._tasks = collections.deque(processors or [])

    def __call__(self, data):
        return functools.reduce(lambda d, p: p(d), self._tasks, data)

    def register(self, func):
        self._tasks.append(func)
        return func

def sanitize_input(data):
    return {k: v.strip() for k, v in data.items() if isinstance(v, str)}

def validate_schema(data):
    required = {'id', 'payload'}
    if not required.issubset(data.keys()):
        raise ValueError(f'missing keys: {required - data.keys()}')
    return data

class PipelineHandler:
    def __init__(self):
        self.pipeline = DataPipeline([sanitize_input, validate_schema])

    def process(self, raw_data):
        try:
            return self.pipeline(raw_data)
        except Exception as e:
            return {'error': str(e), 'status': 'failed'}

if __name__ == '__main__':
    h = PipelineHandler()
    result = h.process({'id': ' 101 ', 'payload': ' data '})
    print(result)