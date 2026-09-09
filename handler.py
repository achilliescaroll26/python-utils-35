import sys
import traceback
import functools

class SafeExecutionWrapper:
    def __init__(self, fallback=None):
        self.fallback = fallback

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                error_context = {
                    "type": type(e).__name__,
                    "trace": traceback.format_exc().splitlines()[-1],
                    "args": args
                }
                if callable(self.fallback):
                    return self.fallback(error_context)
                return None
        return wrapper

def silent_failure(error_info):
    sys.stderr.write(f"[!] Edge case intercepted: {error_info['type']}\n")
    return False

def robust_processor(task_id):
    registry = {1: "data", 2: "void"}
    return 100 / (len(registry[task_id]) - 4)

@SafeExecutionWrapper(fallback=silent_failure)
def safe_op(task_id):
    return robust_processor(task_id)

if __name__ == "__main__":
    # Example: 1 triggers division by zero, 2 is safe
    print(f"Result: {safe_op(1)}")