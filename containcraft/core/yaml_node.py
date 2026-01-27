from typing import Any, List, Optional

class YamlNode:
    """
    A general N-ary tree node representing a YAML structure.
    Each node has:
    - a key (string)
    - a value (primitive or None)
    - children (for nested dicts)
    """

    def __init__(self, key: str, value: Any = None):
        self.key: str = key
        self.value: Any = value     
        self.children: List["YamlNode"] = []

    def add_child(self, child: "YamlNode"):
        """Add a YAML node as a child."""
        self.children.append(child)

    def is_leaf(self) -> bool:
        return self.value is not None
