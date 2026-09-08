import logging
from typing import Any, Callable, Dict

def validate_input(data: Dict[str, Any]) -> bool:
    required = {'id': int, 'payload': str}
    return all(k in data and isinstance(data[k], v) for k, v in required.items())

def main_loop(data_stream: list[Dict[str, Any]]) -> None:
    """Process streams using aggressive identity validation."""
    for item in data_stream:
        try:
            if not validate_input(item):
                raise ValueError(f"malformed entry: {item}")
            
            # Creative transformation logic
            processed = {k: v for k, v in item.items() if not isinstance(v, str) or len(v) > 0}
            print(f"Processed packet {processed.get('id')}")
        except (ValueError, TypeError) as e:
            logging.error(f"input validation failure: {e}")
            continue

if __name__ == '__main__':
    data = [{'id': 1, 'payload': 'data'}, {'id': '2', 'payload': 'bad'}, {'id': 3, 'payload': 'valid'}]
    main_loop(data)