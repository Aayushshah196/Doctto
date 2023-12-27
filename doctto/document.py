from typing import List

from loader import ConfigLoaderFactory
from loguru import logger
from structures import FieldInfo, SyntheticDocument


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

    def synthesize_data(self, copies=None):
        copies = copies or self.document_metadata.get("copies", 1)
        _syn_doc = SyntheticDocument(self.fields)
        synthetic_data = _syn_doc.synthesize_data(copies)
        return synthetic_data

    def __str__(self):
        return (
            f'{self.document_metadata.get("name")} | Fields count: {len(self.fields)}'
        )


if __name__ == "__main__":
    import json

    def main():
        # # Using Yaml Config
        yaml_config_path = "tests/examples/config.yaml"
        yaml_document = Document.create_document(yaml_config_path)
        print("DOCUMENT CONFIG: ", yaml_document)
        logger.info(yaml_document.synthesize_data())
        print("=========================================")

        # # Using Json Config
        # json_config_path = "tests/examples/config.json"
        # json_document = Document.create_document(json_config_path)
        # print("DOCUMENT CONFIG: ", json_document)
        # print("=========================================")

        # Using Dict Config
        # with open(json_config_path, "r") as f:
        #     config = json.load(f)
        # dict_document = Document.create_document(config)
        # print("DOCUMENT CONFIG: ", dict_document)
        # logger.info(dict_document.synthesize_data())
        # print("=========================================")

    main()
