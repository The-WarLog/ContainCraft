from typing import Dict, Any
from .base_schema import BaseSchema
from core.yaml_node import YamlNode
from core.yaml_tree import YamlTree
from ui.inputs import InputHandler

class CustomSchema(BaseSchema):
    name = "custom"

    def guide_user_input(self, ui: InputHandler) -> Dict[str, Any]:
        ui.print_header("Custom YAML Builder")
        root_key = ui.get_string("Root key:")
        tree = YamlTree()
        tree.set_root(root_key)

        if tree.root is None:
            raise ValueError("Root node was not created")

        self._build_obj(ui, tree.root)
        return tree.tree_to_dict()

    def _build_obj(self, ui: InputHandler, parent: YamlNode) -> None:
        while True:
            key = ui.get_string("Add key:")
            t = ui.get_choice("Type:", ["string", "number", "list", "object"])

            if t == "string":
                parent.add_child(YamlNode(key, ui.get_string("Value:")))
            elif t == "number":
                parent.add_child(YamlNode(key, ui.get_number("Number:")))
            elif t == "list":
                parent.add_child(YamlNode(key, ui.get_list("Comma-separated items:")))
            elif t == "object":
                child = YamlNode(key)
                parent.add_child(child)
                self._build_obj(ui, child)

            if not ui.get_yes_no("Add another key here?"):
                break

    def validate(self, data) -> bool:
        return isinstance(data, dict)

    def default_structure(self) -> Dict[str, Any]:
        return {"root": {"sample": 1}}