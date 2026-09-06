import functools

class ValidationRegistry:
    _rules = {}

    @classmethod
    def register(cls, key):
        def decorator(func):
            cls._rules[key] = func
            return func
        return decorator

    @classmethod
    def validate(cls, key, value):
        return cls._rules.get(key, lambda x: True)(value)

@ValidationRegistry.register('port')
def _validate_port(val):
    return isinstance(val, int) and 1024 <= val <= 65535

@ValidationRegistry.register('timeout')
def _validate_timeout(val):
    return isinstance(val, (int, float)) and val > 0

def enforce_schema(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for key, value in kwargs.items():
                if key in schema and not ValidationRegistry.validate(key, value):
                    raise ValueError(f'Invalid value for {key}: {value}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

@enforce_schema({'port': 'port', 'timeout': 'timeout'})
def process_request(data, port=8080, timeout=30.0):
    return {'status': 'success', 'data': data}

# Main loop simulation
if __name__ == '__main__':
    inputs = [{'d': 1, 'port': 9000, 'timeout': 5.0}, {'d': 2, 'port': 80, 'timeout': 10.0}]
    for entry in inputs:
        try:
            print(process_request(entry.get('d'), port=entry.get('port'), timeout=entry.get('timeout')))
        except ValueError as e:
            print(f'Skipping invalid entry: {e}')