# core/yaml_tree.py
from typing import Any, Dict,Optional
from .yaml_node import YamlNode

class YamlTree:
    def __init__(self):
        self.root: YamlNode | None = None
        self._virtual_root: bool = False

    def set_root(self, key: str, value=None):
        self.root = YamlNode(key, value)

    def get_root(self) -> YamlNode | None:
        return self.root

    
    def dict_to_tree(self, key: str, data: Any) -> YamlNode:
        node = YamlNode(key)

        if isinstance(data, dict):
            # nested dict
            for k, v in data.items():
                child = self.dict_to_tree(k, v)
                node.add_child(child)

        else:
            # leaf node
            node.value = data

        return node

    def load_from_dict(self, data: Dict[str, Any]):
        """Build tree from dictionary (YAML loaded)."""
        if len(data) == 1:
            root_key = list(data.keys())[0]
            self.root = self.dict_to_tree(root_key, data[root_key])
            self._virtual_root = False
        else:
            # Allow YAMLs with multiple top-level keys by creating a virtual root
            self.root = YamlNode("root")
            self._virtual_root = True
            for k, v in data.items():
                child = self.dict_to_tree(k, v)
                self.root.add_child(child)

    
    def tree_to_dict(self, node: YamlNode | None = None):
        node = node or self.root

        if node is None:
            raise ValueError("Node cannot be None")

        if node.is_leaf():
            return node.value

        result = {}
        for child in node.children:
            result[child.key] = self.tree_to_dict(child)

        # If we built a virtual root to accommodate multiple top-level keys,
        # unwrap it when converting back to dict for serialization.
        if node is self.root and self._virtual_root:
            return result

        return {node.key: result}
