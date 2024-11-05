import json

class SFNConfigManager:
    def __init__(self, config_path="config/settings.yaml"):
        self.config = self._load_config(config_path)

    def _load_config(self, path):
        with open(path, "r") as file:
            if path.endswith(".json"):
                return json.load(file)
            elif path.endswith(".yaml") or path.endswith(".yml"):
                # TODO 
                pass
        raise ValueError("Unsupported configuration file format")

    def get(self, key, default=None):
        return self.config.get(key, default)