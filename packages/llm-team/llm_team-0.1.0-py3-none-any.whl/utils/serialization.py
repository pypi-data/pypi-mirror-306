import logging
from dataclasses import asdict, dataclass, fields, is_dataclass
from typing import Type, TypeVar

log = logging.getLogger(__name__)

T = TypeVar('T', bound='SerializableMixin')


class SerializableMixin:
    """
    A mixin class that provides serialization and deserialization methods for dataclasses.

    This mixin adds `to_dict` and `from_dict` methods to dataclasses, allowing easy
    conversion between dataclass instances and dictionaries. It also includes a class name
    in the serialized dictionary to support polymorphic deserialization.

    Usage:
        @dataclass
        class MyClass(SerializableMixin):
            field1: int
            field2: str

    Methods:
        to_dict(): Converts the dataclass instance to a dictionary.
        from_dict(cls, d): Creates a dataclass instance from a dictionary.

    Raises:
        TypeError: If a non-dataclass attempts to inherit from this mixin.
        ValueError: If the class name in the deserialized dictionary doesn't match.

    Note:
        This mixin should be listed before other base classes in a multiple inheritance scenario
        to ensure proper method resolution order.
        Only can be used for dataclasses.
    """

    def to_dict(self):
        output = asdict(self)  # type: ignore
        output["class_name"] = self.__class__.__name__
        return output

    @classmethod
    def from_dict(cls: Type[T], d: dict) -> T:
        if d["class_name"] != cls.__name__:
            raise ValueError(
                f"Expected class name {cls.__name__}, got {d['class_name']}")

        d = d.copy()
        d.pop("class_name", None)
        field_names = set(f.name for f in fields(cls))  # type: ignore
        filtered_d = {k: v for k, v in d.items() if k in field_names}

        try:
            return cls(**filtered_d)
        except Exception as E:
            log.exception(f"Error creating {cls.__name__} from dict: {E}")
            raise
