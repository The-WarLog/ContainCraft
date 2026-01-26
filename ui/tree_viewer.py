
from rich.console import Console
from rich.tree import Tree as RichTree
from rich.panel import Panel
from core.yaml_node import YamlNode

console = Console()

def view_tree(node: YamlNode, indent: int = 0):
    """Return a list of lines representing the YAML tree."""
    lines = []
    prefix = "  " * indent

    if node.value is not None:
        # leaf node
        lines.append(f"{prefix}{node.key}: {node.value}")
    else:
        # object node
        lines.append(f"{prefix}{node.key}:")
        for child in node.children:
            lines.extend(view_tree(child, indent + 1))

    return lines


def render_tree_screen(node: YamlNode):
    """Pretty print the YAML tree on the screen."""
    console.clear()
    console.print(Panel("YAML Tree View", style="bold cyan"))
    console.print()

    for line in view_tree(node):
        console.print(f"[white]{line}[/]")

    console.print("\n[yellow]Press Enter to continue...[/]")
    input()
