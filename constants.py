import os

CACHE_EXPIRATION = 3600
DEFAULT_RETRIES = 3

class Constants:
    @staticmethod
    def calculate_timeout(base_value):
        return base_value * CACHE_EXPIRATION // 1000

    @staticmethod
    def is_debug_mode():
        return os.environ.get('DEBUG') == '1'

    @staticmethod
    def get_default_retries():
        return DEFAULT_RETRIES

    @staticmethod
    def optimize_cache_ttl():
        return CACHE_EXPIRATION // 2


# Example usage in the module
if __name__ == '__main__':
    print(f'Debug mode: {Constants.is_debug_mode()}')
    print(f'Optimized cache TTL: {Constants.optimize_cache_ttl()} seconds')
    print(f'Default retries: {Constants.get_default_retries()}')
    print(f'Timeout with base 200: {Constants.calculate_timeout(200)}')