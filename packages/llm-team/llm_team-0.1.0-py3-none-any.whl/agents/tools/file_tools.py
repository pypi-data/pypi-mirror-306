import ast
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel

from src.agents.tools import AnthropicTool
from src.agents.tools.utils.hierachal_retriever import HierarchicalCodebaseViewer

__all__ = [
    "ls_tool",
    "file_write_tool",
    "file_read_tool",
    "file_modification_tool",
    "view_project_structure_tool",
    "get_symbol_info_tool",
]


def ls(directory: str, show_hidden_files: bool):
    files = os.listdir(directory)
    if not show_hidden_files:
        files = [f for f in files if not f.startswith(".")]
    return "\n".join(files)


ls_tool = AnthropicTool(name="List_Files",
                        function=ls,
                        description="List all files in a directory.")


def file_writer(file_path: str, content: str):
    try:
        p = Path(file_path)
        p.parent.mkdir(exist_ok=True, parents=True)

        with open(file_path, "w") as f:
            f.write(content)
            return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"


file_write_tool = AnthropicTool(name="Write_To_File",
                                function=file_writer,
                                description="Write to a file")


def file_reader(file_path: str):
    try:
        path = Path(file_path)
        return path.read_text()
    except Exception as e:
        return f"Error reading file: {str(e)}"


file_read_tool = AnthropicTool(name="Read_File",
                               function=file_reader,
                               description="""Read a file's contents""")


def modify_file(
    file_path: str,
    line_number: int,
    num_lines: int,
    new_data: str,
) -> None:
    file_path = file_path
    line_number = line_number
    num_lines = num_lines
    new_data = new_data

    with open(file_path, "r") as file:
        lines = file.readlines()
    start_line = line_number - 1
    end_line = start_line + num_lines

    lines[start_line:end_line] = [new_data + "\n"]

    with open(file_path, "w") as file:
        file.writelines(lines)


file_modification_tool = AnthropicTool(
    name="Modify_File",
    function=modify_file,
    description="""Modify a section of a file's contents

Args:

file_path: The path to the file that will be modified.

line_number: The starting line number where the modification will begin (1-indexed).

num_lines: The number of lines to be replaced in the file.

new_data: The new content to be inserted in place of the removed lines.""",
)


def view_project_structure(file_path: str):
    viewer = HierarchicalCodebaseViewer(file_path)

    viewer.build_hierarchy()
    return viewer.generate_hierarchy()


view_project_structure_tool = AnthropicTool(
    name="View_Project_Structure",
    function=view_project_structure,
    description=
    """View the directory structure of a code base given the root directory of the code base.""",
)


class NodeInfoResultType(Enum):
    SOURCE_CODE_FOUND = "SOURCE_CODE_FOUND"
    REFERENCE_FOUND = "REFERENCE_FOUND"
    NODE_NOT_FOUND = "NODE_NOT_FOUND"


@dataclass
class NodeInfoResult:
    result_type: NodeInfoResultType
    node_name: str
    file_path: str
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    code: Optional[str] = None

    def __str__(self):
        result = f"NodeInfoResult: {self.result_type.value}, node={self.node_name}, file={self.file_path}\n"

        if self.result_type != NodeInfoResultType.NODE_NOT_FOUND:
            result += f", lines={self.start_line}-{self.end_line}\n"
        if self.code:
            result += self.code + "\n\n"
        return result


def get_identifier_info(file_path: str, identifier: str) -> NodeInfoResult:
    with open(file_path, "r") as file:
        source = file.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if (isinstance(node,
                       (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == identifier):
            start_line = node.lineno
            end_line = node.end_lineno if hasattr(
                node, "end_lineno") else node.lineno
            code = ast.unparse(node)
            return NodeInfoResult(
                result_type=NodeInfoResultType.SOURCE_CODE_FOUND,
                node_name=identifier,
                file_path=file_path,
                start_line=start_line,
                end_line=end_line,
                code=code,
            )
        elif isinstance(node, ast.Name) and node.id == identifier:
            return NodeInfoResult(
                result_type=NodeInfoResultType.REFERENCE_FOUND,
                node_name=identifier,
                file_path=file_path,
                start_line=node.lineno,
                end_line=node.lineno,
                code=identifier,
            )
    return NodeInfoResult(
        result_type=NodeInfoResultType.NODE_NOT_FOUND,
        node_name=identifier,
        file_path=file_path,
    )


get_symbol_info_tool = AnthropicTool(
    name="Get_Identifier_Info",
    function=get_identifier_info,
    description=
    """Extracts the source code and line range of a specified Python class, function, or async function from a given file.""",
)

if __name__ == "__main__":
    v = get_identifier_info(
        file_path=
        r"D:\projects\testbed\open-llm-swe\src\agents\tools\file_tools.py",
        identifier="get_node_info",
    )
    print(v)
