from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from providers import SYNTHETIC_GENERATOR


@dataclass
class BBox:
    x0: int
    y0: int
    x2: int
    y2: int

    @classmethod
    def empty_bbox(cls):
        return cls(0, 0, 0, 0)

    def to_tuple(self):
        return (self.x0, self.y0, self.x2, self.y2)

    def to_dict(self):
        return self.__dict__()

    def __hash__(self) -> int:
        return hash(self.to_dict())

    def __str__(self):
        return self.to_tuple()

    def __repr__(self):
        return str(self.to_tuple())

    @property
    def top_left(self):
        return (self.x0, self.y0)

    @property
    def bottom_right(self):
        return (self.x2, self.y2)


@dataclass
class DataType:
    value: str = "string"


@dataclass
class Alignment:
    "Alignment is between 0 & 1. 0 being the left and 1 being the right"
    value: int = 0


@dataclass
class Spacing:
    value: int = 0


@dataclass
class FontSize:
    value: int = 14


@dataclass
class FontType:
    value: str = "Arial"


class FakerStrategy:
    """
    Represents a strategy for generating values using the Faker library based on data type.
    """

    _DATA_GENERATOR = SYNTHETIC_GENERATOR

    def __init__(self, data_type):
        self.generation_method = FakerStrategy.default_factory(data_type)

    @staticmethod
    def default_factory(data_type) -> str:
        """
        Generate a Faker value based on the specified data type.

        Returns:
            str: The generated Faker value.
        """
        return FakerStrategy._DATA_GENERATOR.get(data_type.value)

    def generate_value(self):
        return self.generate_method()


@dataclass
class FieldMetadata:
    """
    Represents metadata for a field in a document.

    Attributes:
        custom_attributes (Dict[str, str]): Arbitrary key-value pairs for custom metadata.
    """

    custom_attributes: Dict[str, Any] = field(default_factory=dict)

    def __setitem__(self, index, value):
        self.custom_attributes[index] = value

    def __getitem__(self, index):
        return self.custom_attributes.get(index)


@dataclass
class FieldInfo:
    """
    Represents information about a field in a document.

    Attributes:
        name (str): The name of the field.
        prefix (str): The prefix to be added to the field value.
        postfix (str): The postfix to be added to the field value.
        bbox (BBox): The bounding box specifying the position of the field.
        data_type (DataType): The data type of the field.
        value (str): The actual value of the field.
        multiline (bool): True if the field supports multiline text, False otherwise.
        fontsize (FontSize): The font size of the field.
        h_align (Alignment): Horizontal alignment of the field.
        v_align (Alignment): Vertical alignment of the field.
        metadata (FieldMetadata): Additional metadata for the field.
    """

    name: str
    prefix: str = ""
    postfix: str = ""
    value: str = ""
    bbox: BBox = field(default_factory=lambda: BBox.empty_bbox())
    data_type: DataType = field(default_factory=DataType)
    multiline: bool = False
    fontsize: FontSize = field(default_factory=FontSize)
    h_align: Alignment = field(default_factory=Alignment)
    v_align: Alignment = field(default_factory=Alignment)
    spacing: Spacing = field(default_factory=Spacing)
    metadata: FieldMetadata = field(default_factory=FieldMetadata)
    __synthetic_generation_method = None

    def __post_init__(self):
        ## Standardizing the bbox attribute
        if not isinstance(self.bbox, BBox):
            if isinstance(self.bbox, (Tuple, List)):
                self.bbox = BBox(*self.bbox)
            elif isinstance(self.bbox, dict):
                self.bbox = BBox(**self.bbox)
        ## Standardizing the data_type attribute
        if not isinstance(self.data_type, DataType):
            self.data_type = DataType(self.data_type)
        ## Standardizing the fontsize attribute
        if not isinstance(self.data_type, FontSize):
            self.fontsize = FontSize(self.fontsize)
        ## Standardizing the h_align attribute
        if not isinstance(self.h_align, Alignment):
            self.h_align = Alignment(self.h_align)
        ## Standardizing the v_align attribute
        if not isinstance(self.v_align, Alignment):
            self.v_align = Alignment(self.v_align)
        ## Standardizing the spacing attribute
        if not isinstance(self.v_align, Spacing):
            self.spacing = Spacing(self.spacing)

        self.__synthetic_generation_method = FakerStrategy.default_factory(
            self.data_type
        )

    def __str__(self):
        return f"( Name: {self.name} | Data Type: {self.data_type.value} )"

    def __repr__(self):
        return f"( Name: {self.name} | Data Type: {self.data_type.value} )"

    @property
    def text(self):
        return self.prefix + self.value + self.postfix

    def synthesize(self):
        self.value = self.__synthetic_generation_method()

    def __setitem__(self, index, value):
        if hasattr(self, index):
            setattr(self, index, value)
        else:
            self.metadata[index] = value

    def __getitem__(self, index):
        if hasattr(self, index):
            return getattr(self, index)
        return self.metadata.get(index)

    def set_metadata(self, custom_key, custom_value):
        self.metadata.add_key_value(custom_key, custom_value)

    def to_dict(self):
        data = {
            "name": self.name,
            "value": self.text,
            "data_type": self.data_type.value,
            "bbox": self.bbox.to_tuple(),
        }
        return data


@dataclass
class SyntheticDocument:
    fields: List[FieldInfo] = field(default_factory=[])

    def synthesize_data(self, copies: int = 1):
        data = []
        for i in range(copies):
            _single_doc = {}
            for field in self.fields:
                field.synthesize()
                _single_doc[field.name] = field.to_dict()
            data.append(_single_doc)
        return data


if __name__ == "__main__":
    name_field = FieldInfo("name", data_type=DataType("postalcode"))
    print(name_field)
    print("=============================================")
    print("TEXT: ", name_field.text)
    name_field.synthesize()
    print("WITH VALUE, TEXT: ", name_field.text)
    print("=============================================")
    name_field.prefix = "$ "
    print("WITH PREFIX, TEXT: ", name_field.text)
    print("=============================================")
    name_field.postfix = " |-"
    print("WITH POSTFIX, TEXT: ", name_field.text)
