import yaml
import os
import copy
import tempfile
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from typing import Any

console = Console()

def _get_by_path(data, path):
    parts = _split_path(path)
    cur = data
    for p in parts:
        if isinstance(cur, dict):
            cur = cur[p]
        elif isinstance(cur, list):
            cur = cur[int(p)]
        else:
            raise KeyError(f"Cannot navigate into {type(cur).__name__}")
    return cur

def _set_by_path(data, path, value):
    parts = _split_path(path)
    cur = data
    for p in parts[:-1]:
        if isinstance(cur, dict):
            cur = cur[p]
        elif isinstance(cur, list):
            cur = cur[int(p)]
    cur[parts[-1]] = value

def _del_by_path(data, path):
    parts = _split_path(path)
    cur = data
    for p in parts[:-1]:
        if isinstance(cur, dict):
            cur = cur[p]
        elif isinstance(cur, list):
            cur = cur[int(p)]
    del cur[parts[-1]]

def _split_path(path):
    """Parse path like 'a.b.c' or 'arr[0].field'"""
    segments = []
    for seg in path.split("."):
        if "[" in seg and seg.endswith("]"):
            name, idx = seg[:-1].split("[")
            if name:
                segments.append(name)
            segments.append(idx)
        else:
            segments.append(seg)
    return segments

def _pretty(data):
    return yaml.safe_dump(data, sort_keys=False, default_flow_style=False)

def _preview(old, new):
    console.print("\n[bold red]BEFORE[/]")
    console.print(Panel(Syntax(_pretty(old), "yaml", theme="monokai"), border_style="red"))
    console.print("\n[bold green]AFTER[/]")
    console.print(Panel(Syntax(_pretty(new), "yaml", theme="monokai"), border_style="green"))

def _show_keys(data, prefix=""):
    """Show available keys in a dict/list"""
    if isinstance(data, dict):
        for key in data.keys():
            console.print(f"  [cyan]{prefix}{key}[/]")
    elif isinstance(data, list):
        for i in range(len(data)):
            console.print(f"  [cyan]{prefix}[{i}][/]")

def edit_yaml_session(data: dict | None) -> dict | None:
    original = data
    working = copy.deepcopy(original)
    history = []

    while True:
        console.clear()
        console.print(Panel("YAML Editor", style="bold cyan"))
        console.print(Syntax(_pretty(working), "yaml", theme="monokai"))
        console.print("\n[bold]Actions:[/]\n"
                      "1) Set value at path\n"
                      "2) Append to list\n"
                      "3) Delete key\n"
                      "4) Show available keys\n"
                      "5) Undo last change\n"
                      "6) Preview diff & save\n"
                      "7) Cancel")

        choice = console.input("[bold white]Enter choice number> [/]").strip()

        if choice == "1":
            console.print("[cyan]Examples: services.kafka.restart, services.kafka.environment.KAFKA_BROKER_ID[/]")
            path = console.input("Full path to value> ").strip()
            val = console.input("New value (string)> ")
            try:
                history.append(copy.deepcopy(working))
                _set_by_path(working, path, val)
                console.print(f"[green]✓ Updated {path}[/]")
                input("Press Enter to continue")
            except Exception as e:
                console.print(f"[red]Error: {e}[/]")
                working = history.pop()  # rollback
                input("Press Enter to continue")

        elif choice == "2":
            path = console.input("List path (e.g., services.kafka.ports)> ").strip()
            val = console.input("Value to append> ")
            try:
                history.append(copy.deepcopy(working))
                lst = _get_by_path(working, path)
                if not isinstance(lst, list):
                    console.print("[red]Not a list[/]")
                    working = history.pop()
                else:
                    lst.append(val)
                    console.print(f"[green]✓ Appended to {path}[/]")
                    input("Press Enter to continue")
            except Exception as e:
                console.print(f"[red]Error: {e}[/]")
                working = history.pop()
                input("Press Enter to continue")

        elif choice == "3":
            path = console.input("Path to delete> ").strip()
            try:
                history.append(copy.deepcopy(working))
                _del_by_path(working, path)
                console.print(f"[green]✓ Deleted {path}[/]")
                input("Press Enter to continue")
            except Exception as e:
                console.print(f"[red]Error: {e}[/]")
                working = history.pop()
                input("Press Enter to continue")

        elif choice == "4":
            path = console.input("Path to explore (leave empty for root)> ").strip()
            try:
                if path:
                    cur = _get_by_path(working, path)
                else:
                    cur = working
                console.clear()
                console.print(Panel(f"Available keys in {path or 'root'}:", style="bold blue"))
                _show_keys(cur, "")
                if isinstance(cur, (dict, list)):
                    console.print(f"\n[yellow]Preview:[/]")
                    console.print(Syntax(_pretty(cur), "yaml", theme="monokai"))
                input("\nPress Enter to continue")
            except Exception as e:
                console.print(f"[red]Error: {e}[/]")
                input("Press Enter to continue")

        elif choice == "5":
            if history:
                working = history.pop()
                console.print("[green]✓ Undone[/]")
                input("Press Enter to continue")
            else:
                console.print("[yellow]Nothing to undo[/]")
                input("Press Enter to continue")

        elif choice == "6":
            console.clear()
            _preview(original, working)
            if console.input("\n[bold white]Save changes? (y/n)> [/]").lower().startswith("y"):
                return working
            else:
                console.print("[yellow]Changes not saved[/]")
                input("Press Enter to continue")

        elif choice == "7":
            console.print("[bold yellow]Discarding changes[/]")
            return None

        else:
            console.print("[red]Invalid choice[/]")
            input("Press Enter to continue")


'''def _get_by_path(data,path):
    parts=_split_path(path)
    cur=data
    for p in parts:
        cur=cur[p]
    return cur
def _set_by_path(data,path,value):
    parts=_split_path(path)
    cur=data
    for p in parts[:-1]:
        cur=cur[p]
    cur[parts[-1]]=value
def _del_by_path(data,path):
    parts=_split_path(path)
    cur=data
    for p in parts[::-1]:
        cur=cur[p]
    del cur[parts[-1]]

def _split_path(path):
    segments = []
    for seg in path.split("."):
        if "[" in seg and seg.endswith("]"):
            name, idx = seg[:-1].split("[")
            segments.append(name)
            segments.append(int(idx))
        else:
            segments.append(seg)
    return segments

def _pretty(data):
    return yaml.dump(data=data,sort_keys=False,default_flow_style=False)

def _preview(old,new):
    console.print(Panel("Before Edit",style="red"))
    console.print(Syntax(_pretty(old),"yaml",theme="monokai"))
    console.print(Panel("After Edit",style="bold green"))
    console.print(Syntax(_pretty(new),"yaml",theme="monokai"))
def edit_yaml_session(data: dict) -> dict | None:
    original = data
    working = copy.deepcopy(original)
    history = []

    while True:
        console.clear()
        console.print(Panel("YAML Editor", style="bold cyan"))
        console.print(Syntax(_pretty(working), "yaml", theme="monokai"))
        console.print("\n[bold]Actions:[/]\n"
                      "1) Set value\n"
                      "2) Append to list\n"
                      "3) Delete key\n"
                      "4) Undo last change\n"
                      "5) Preview diff & save\n"
                      "6) Cancel")

        choice = console.input("[bold white]Enter choice number> [/]").strip()

        if choice == "1":
            path = console.input("Path (e.g., services.kafka.restart)> ").strip()
            val  = console.input("New value (stored as string)> ")
            history.append(copy.deepcopy(working))
            _set_by_path(working, path, val)

        elif choice == "2":
            path = console.input("List path (e.g., items)> ").strip()
            val  = console.input("Value to append (string)> ")
            history.append(copy.deepcopy(working))
            lst = _get_by_path(working, path)
            if not isinstance(lst, list):
                console.print("[red]Not a list[/]")
                working = history.pop()  # rollback
            else:
                lst.append(val)

        elif choice == "3":
            path = console.input("Path to delete> ").strip()
            history.append(copy.deepcopy(working))
            try:
                _del_by_path(working, path)
            except Exception as e:
                console.print(f"[red]Delete failed: {e}[/]")
                working = history.pop()

        elif choice == "4":
            if history:
                working = history.pop()
            else:
                console.print("[yellow]Nothing to undo[/]")
                console.input("Enter to continue")

        elif choice == "5":
            console.clear()
            _preview(original, working)
            if console.input("\nSave changes? (y/n)> ").lower().startswith("y"):
                return working  # caller will write to file
        elif choice == "6":
            return None
        else:
            console.print("[red]Invalid choice[/]")
        


'''