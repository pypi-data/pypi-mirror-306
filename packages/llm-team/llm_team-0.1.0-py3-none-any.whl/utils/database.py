from dataclasses import dataclass, fields
from typing import Any, Dict, Type

from peewee import *

db = SqliteDatabase(
    'example.db')  # You can change this to your preferred database

model_registry = {}


def dataclass_to_peewee_model(cls: Type[Any]) -> Type[Model]:
    if not dataclass(cls):
        raise TypeError("Input must be a dataclass")

    if cls.__name__ in model_registry:
        return model_registry[cls.__name__]

    class Meta:
        database = db
        table_name = cls.__name__.lower()

    attributes = {}
    for field in fields(cls):
        field_type = field.type
        if field_type == int:
            attributes[field.name] = IntegerField()
        elif field_type == float:
            attributes[field.name] = FloatField()
        elif field_type == str:
            attributes[field.name] = CharField()
        elif field_type == bool:
            attributes[field.name] = BooleanField()
        elif isinstance(field_type, type) and dataclass(field_type):
            # Handle foreign key relationship
            referenced_model = dataclass_to_peewee_model(field_type)
            attributes[field.name] = ForeignKeyField(
                referenced_model, backref=cls.__name__.lower() + 's')
        else:
            attributes[field.name] = TextField(
            )  # Default to TextField for complex types

    attributes['Meta'] = Meta

    model_name = f"{cls.__name__}Model"
    model = type(model_name, (Model, ), attributes)
    model_registry[cls.__name__] = model
    return model
