from .yaml_node import YamlNode

def render_tree(node: YamlNode, indent: str = "") -> str:
    """Render the YAML tree as indented lines.

    Note: we must append child blocks as lists of lines, not extend with the
    raw string, otherwise Python will iterate characters and print vertically.
    """
    label = f"{node.key}: {node.value}" if node.is_leaf() else node.key
    lines = [indent + label]

    for child in node.children:
        child_block = render_tree(child, indent + "  ")
        lines.extend(child_block.splitlines())

    return "\n".join(lines)
