import inspect
import logging
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Type

from pydantic import BaseModel, create_model

from src.utils.module_exports import get_module_exports

log = logging.getLogger(__name__)


class AnthropicToolDTO(BaseModel):
    """
    Data Transfer Object representing the serializable fields of an AnthropicTool.

    This model serves as a schema for serialization and deserialization of AnthropicTool instances.
    It includes only the fields that should be persisted when serializing an AnthropicTool.
    """

    name: str
    description: str
    input_schema: dict[str, Any]
    function: str  # Store the function's qualified name as a string

    def to_dict(self):
        return {
            "class_name": self.__class__.__name__,
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "function": self.function.__qualname__,
        }

    @classmethod
    def from_dict(cls,
                  data: dict,
                  possible_tools: Optional[dict] = None) -> "AnthropicTool":
        """
        Create an AnthropicTool instance from a dictionary representation.

        :param data: Dictionary containing the serialized AnthropicTool data
        :param possible_tools: dict of tool name (str): anthropic tool to be instantiated. defaults to all exported tools if not set.
        """
        # Validate the input data using the AnthropicToolModel

        validated_data = cls(**data)

        all_tools = possible_tools or get_all_exported_tools()

        # Look up the tool in the all_tools dictionary

        tool = all_tools.get(validated_data.name)
        if tool is None:
            raise ValueError(f"Tool not found: {validated_data.name}")
        # Update the tool's description and input_schema if they've changed

        tool.description = validated_data.description
        tool.input_schema = validated_data.input_schema

        return tool

    class Config:
        extra = "ignore"  # This will ignore any extra fields during deserialization


@dataclass
class AnthropicTool():
    name: str
    description: str
    function: Callable

    def __post_init__(self):
        self.input_schema: dict[str,
                                Any] = self._generate_schema(self.function)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: "AnthropicTool") -> bool:
        return isinstance(other, AnthropicTool) and self.name == other.name

    def __str__(self) -> str:
        return f"Tool Name: {self.name}, Tool Description: {self.description}"

    def format_for_anthropic_api(self):
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }

    def _generate_schema(self, f: Callable):
        return get_model_schema(generate_pydantic_model(f))


def generate_pydantic_model(func: Callable) -> Type[BaseModel]:
    signature = inspect.signature(func)
    field_definitions = {}

    for param_name, param in signature.parameters.items():
        if param.annotation is inspect.Parameter.empty:
            raise ValueError(
                f"Parameter '{param_name}' is missing a type annotation")
        field_definitions[param_name] = (param.annotation, ...)
    model_name = f"{func.__name__.capitalize()}Model"
    model = create_model(model_name, **field_definitions)

    if not issubclass(model, BaseModel):
        raise TypeError(f"Created model is not a subclass of BaseModel")
    return model


def get_model_schema(model: Type[BaseModel]) -> dict:
    if hasattr(model, "model_json_schema"):  # Pydantic v2
        return model.model_json_schema()
    elif hasattr(model, "schema"):  # Pydantic v1
        return model.schema()
    else:
        raise AttributeError(
            "Model doesn't have 'model_json_schema' or 'schema' method")


def get_all_exported_tools(tool_packages: Optional[List[str]] = None):
    """
    Retrieve all exported AnthropicTool instances from specified Python packages.

    This function iterates through a list of package names, imports each package,
    and collects all exported objects that are instances of AnthropicTool.
    It filters out class definitions and only includes instantiated tools.

    Args:
        tool_packages (Optional[List[str]]): A list of package names to search for tools.
            If None, defaults to ['src.agents.tools.file_tools',
            'src.agents.tools.mathematical'].

    Returns:
        Dict[str, AnthropicTool]: A dictionary where keys are the names of the exported
        tools and values are the corresponding AnthropicTool instances.

    Raises:
        ImportError: If any of the specified packages cannot be imported.
        AttributeError: If get_module_exports function is not defined or accessible.
    """

    tool_packages = tool_packages or [
        "src.agents.tools.file_tools",
        "src.agents.tools.mathematical",
    ]

    all_exports = {}
    for tool_package in tool_packages:
        # Get exports as a dictionary of name-object pairs

        all_exports.update(get_module_exports(tool_package, as_dict=True))
    return {
        v.name: v
        for v in all_exports.values()
        if isinstance(v, AnthropicTool) and not inspect.isclass(v)
    }


def get_tool_by_name(tool_name: str,
                     tools: Optional[List[AnthropicTool]] = None):
    if not tools:
        tools = list(get_all_exported_tools().values())
    try:
        return next(i for i in tools
                    if i.name.lower().strip() == tool_name.lower().strip())
    except Exception as e:
        log.exception(e)
        return


2
