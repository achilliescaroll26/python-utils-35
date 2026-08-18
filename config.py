import json
import os

class ConfigError(Exception):
    pass

class Config:
    def __init__(self, filepath):
        self.filepath = filepath
        self.config_data = {}
        self.load_config()

    def load_config(self):
        try:
            with open(self.filepath, 'r') as file:
                self.config_data = json.load(file)
        except FileNotFoundError:
            raise ConfigError(f'Configuration file not found: {self.filepath}')
        except json.JSONDecodeError:
            raise ConfigError(f'Error decoding JSON from file: {self.filepath}')
        except Exception as e:
            raise ConfigError(f'Unexpected error when loading config: {e}')

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def set(self, key, value):
        self.config_data[key] = value
        self.save_config()

    def save_config(self):
        try:
            with open(self.filepath, 'w') as file:
                json.dump(self.config_data, file, indent=4)
        except Exception as e:
            raise ConfigError(f'Failed to save config: {e}')

# Example usage:
# config = Config('config.json')
# config.set('key', 'value')
# print(config.get('key'))
