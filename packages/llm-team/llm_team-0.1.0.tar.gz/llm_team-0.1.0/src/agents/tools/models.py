from peewee import *

from src.database.db import BaseModel


class AnthropicToolFunctionModel(BaseModel):
    name = CharField()


class AnthropicToolModel(BaseModel):
    name: str
    description: str


class FunctionToToolLink(BaseModel):
    function = ForeignKeyField(AnthropicToolFunctionModel)
    tool = ForeignKeyField(AnthropicToolModel)
