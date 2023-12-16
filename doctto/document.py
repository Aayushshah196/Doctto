from typing import List

from loader import ConfigLoaderFactory
from structures import FieldInfo


class Document:
    def __init__(self, document_metadata, fields: List[FieldInfo] = []):
        self.document_metadata = document_metadata
        self.fields = fields

    @classmethod
    def create_document(cls, source):
        config_loader = ConfigLoaderFactory.create_loader(source)
        if not config_loader:
            raise Exception("Improper source to load config")
        config = config_loader.load_config()
        fields = config.pop("fields", [])
        return cls(document_metadata=config, fields=fields)

    def __str__(self):
        return (
            f'{self.document_metadata.get("name")} | Fields count: {len(self.fields)}'
        )


if __name__ == "__main__":
    import json

    def main():
        # Using Yaml Config
        yaml_config_path = "tests/examples/config.yaml"
        yaml_document = Document.create_document(yaml_config_path)
        print("DOCUMENT CONFIG: ", yaml_document)
        print("=========================================")

        # Using Json Config
        json_config_path = "tests/examples/config.json"
        json_document = Document.create_document(json_config_path)
        print("DOCUMENT CONFIG: ", json_document)
        print("=========================================")

        # Using Dict Config
        with open(json_config_path, "r") as f:
            config = json.load(f)
        dict_document = Document.create_document(config)
        print("DOCUMENT CONFIG: ", dict_document)
        print("=========================================")

    main()
