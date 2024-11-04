import ast
import fnmatch
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Union

from src.config.project_paths import package_root

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)


class CodeNode:

    def __init__(self, name: str, type: str, docstring: Optional[str] = None):
        self.name = name
        self.type = type
        self.docstring = docstring
        self.children: List[CodeNode] = []

    def add_child(self, child: 'CodeNode'):
        self.children.append(child)

    def __repr__(self):
        return f"{self.type}: {self.name}"


class HierarchicalCodebaseViewer:

    def __init__(self, root_dir: str):
        self.additional_resource_dir = package_root / 'resources'

        if not Path(root_dir).exists():
            raise FileNotFoundError(f"{root_dir} does not exist.")

        self.root_dir = root_dir
        self.hierarchy = CodeNode(os.path.basename(root_dir), "project")
        self.ignore_patterns = [
            *self._parse_gitignore(
                self.additional_resource_dir / 'standard_gitignore.txt'),
            *self._parse_project_gitignore()
        ]

        log.debug(f'ignore patterns: {self.ignore_patterns}')

    def _parse_gitignore(self, filepath: Path):
        ignore_patterns = []
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        ignore_patterns.append(line)

        return ignore_patterns

    def _parse_project_gitignore(self) -> List[str]:
        return self._parse_gitignore(Path(self.root_dir) / '.gitignore')

    def _should_ignore(self, path: str) -> bool:
        # Get the path relative to the root directory
        rel_path = os.path.relpath(path, self.root_dir)

        # Split the path into parts
        path_parts = rel_path.split(os.sep)

        for pattern in self.ignore_patterns:
            # Check if the pattern ends with '/' (directory pattern)
            if pattern.endswith('/'):
                if any(
                        fnmatch.fnmatch(
                            os.path.join(*path_parts[:i + 1]) + '/', pattern)
                        for i in range(len(path_parts))):
                    return True
            # For file patterns, check each possible file path
            elif any(
                    fnmatch.fnmatch(os.path.join(*path_parts[:i + 1]), pattern)
                    for i in range(len(path_parts))):
                return True

        return False

    def build_hierarchy(self):
        for root, dirs, files in os.walk(self.root_dir):
            # Remove ignored directories
            dirs[:] = [
                d for d in dirs
                if not self._should_ignore(os.path.join(root, d))
            ]

            for file in files:
                # print(root, file)
                if file.endswith('.py') and not self._should_ignore(
                        os.path.join(root, file)):
                    file_path = os.path.join(root, file)
                    file_node = self._parse_file(file_path)
                    if file_node:
                        self._add_to_hierarchy(file_node, root)

    def _parse_file(self, file_path: str) -> Optional[CodeNode]:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
        except UnicodeDecodeError:
            return

        tree = ast.parse(content)
        file_node = CodeNode(os.path.basename(file_path), "file")

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_node = CodeNode(node.name, "class",
                                      ast.get_docstring(node))
                file_node.add_child(class_node)
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_node = CodeNode(item.name, "method",
                                               ast.get_docstring(item))
                        class_node.add_child(method_node)
            elif isinstance(node, ast.FunctionDef):
                func_node = CodeNode(node.name, "function",
                                     ast.get_docstring(node))
                file_node.add_child(func_node)
            elif isinstance(node, ast.AsyncFunctionDef):
                func_node = CodeNode(node.name, "async function",
                                     ast.get_docstring(node))
                file_node.add_child(func_node)

        return file_node

    def _add_to_hierarchy(self, file_node: CodeNode, file_path: str):
        parts = os.path.relpath(file_path, self.root_dir).split(os.sep)
        current = self.hierarchy
        for part in parts:
            found = next(
                (child for child in current.children if child.name == part),
                None)
            if not found:
                new_node = CodeNode(part, "directory")
                current.add_child(new_node)
                current = new_node
            else:
                current = found
        current.add_child(file_node)

    def generate_hierarchy(self,
                           node: Optional[CodeNode] = None,
                           indent: int = 0) -> str:
        if node is None:
            node = self.hierarchy

        result = []
        result.append('  ' * indent + str(node))

        for child in node.children:
            result.append(self.generate_hierarchy(child, indent + 1))

        return '\n'.join(result)


# Usage
if __name__ == "__main__":
    # viewer = HierarchicalCodebaseViewer(r"D:\projects\homeserver\services\telegram_bots\monthly_expense_analyser")
    viewer = HierarchicalCodebaseViewer(
        r"C:\Users\zhuwe\OneDrive\Desktop\projects\testbed\MLE-agent")

    viewer.build_hierarchy()
    print(viewer.generate_hierarchy())
