import json
from abc import ABC, abstractmethod

import yaml
from loguru import logger
from structures import FieldInfo


# ConfigLoader is responsible for loading configuration from various sources.
class ConfigLoader(ABC):
    def __init__(self, source):
        self.source = source

    @abstractmethod
    def load_config_from_source(self):
        raise NotImplementedError

    def map_config(self, config):
        return config

    def standardize_fields(self, config):
        fields = config.get("fields")
        if not fields:
            return config

        fields = [FieldInfo(**field) for field in fields]
        config["fields"] = fields
        return config

    def load_config(self):
        config = self.load_config_from_source()
        logger.debug(f"LOADED CONFIG FROM SOURCE: {config}")
        config = self.map_config(config)
        config = self.standardize_fields(config)
        return config


class YamlConfigLoader(ConfigLoader):
    def load_config_from_source(self):
        with open(self.source, "r") as file:
            return yaml.safe_load(file)


class JsonConfigLoader(ConfigLoader):
    def load_config_from_source(self):
        with open(self.source, "r") as file:
            return json.load(file)


class DictConfigLoader(ConfigLoader):
    def load_config_from_source(self):
        return self.source


class ConfigLoaderFactory:
    @staticmethod
    def create_loader(source):
        if isinstance(source, str):
            if source.lower().endswith(("yaml", "yml")):
                return YamlConfigLoader(source)
            elif source.lower().endswith("json"):
                return JsonConfigLoader(source)
        elif isinstance(source, dict):
            return DictConfigLoader(source)
        return None


if __name__ == "__main__":

    def main():
        # Client Code
        # Using Yaml Config
        yaml_config_path = "tests/examples/config.yaml"
        yaml_loader = ConfigLoaderFactory.create_loader(yaml_config_path)
        yaml_field_info = yaml_loader.load_config()
        print("YAML Config:", yaml_field_info)
        print("=========================================")

        # Using Json Config
        json_config_path = "tests/examples/config.json"
        json_loader = ConfigLoaderFactory.create_loader(json_config_path)
        json_field_info = json_loader.load_config()
        print("JSON Config:", json_field_info)
        print("=========================================")

        # Using Dict Config
        with open(json_config_path, "r") as f:
            config = json.load(f)
        dict_loader = ConfigLoaderFactory.create_loader(config)
        dict_field_info = dict_loader.load_config()
        print("Dict Config:", dict_field_info)
        print("=========================================")

    main()
