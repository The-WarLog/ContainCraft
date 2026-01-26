from rich.console import Console
from rich.align import Align
from yaml_cli.banner import print_ascii_banner
from ui.menu import Menu

console = Console()

def main():
    console.clear()
    banner = print_ascii_banner()
    for line in banner.splitlines():
        console.print(Align.center(f"[bold magenta]{line}[/]"))
    console.print(Align.center("[italic blue]Contain With Ease[/]"))
    console.print()

    menu = Menu()
    menu.main_menu()

if __name__ == "__main__":
    main()


