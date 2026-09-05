import logging

class DataProcessor:
    def __init__(self, schema):
        self.schema = schema
        self.logger = logging.getLogger(__name__)

    def validate(self, item):
        for key, expected_type in self.schema.items():
            val = item.get(key)
            if not isinstance(val, expected_type):
                raise ValueError(f"Invalid type for {key}: expected {expected_type.__name__}")
        return True

    def run(self, input_data):
        results = []
        for entry in input_data:
            try:
                if self.validate(entry):
                    processed = entry.get('value', 0) * 2
                    results.append(processed)
            except (ValueError, TypeError) as e:
                self.logger.warning(f"Skipping invalid entry {entry}: {e}")
        return results

if __name__ == '__main__':
    schema = {'id': int, 'value': int}
    proc = DataProcessor(schema)
    data = [{'id': 1, 'value': 10}, {'id': 2, 'value': 'bad'}, {'id': 3, 'value': 30}]
    print(proc.run(data))