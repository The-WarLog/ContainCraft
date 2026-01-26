from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
import os

console = Console()

class InputHandler:
    def print_header(self, text):
        console.clear()
        console.print(Panel(text, style="bold cyan", expand=False))
        console.print()

    def get_string(self, prompt):
        return Prompt.ask(f"[bold white]{prompt}[/]").strip()

    def get_number(self, prompt, min_val=None, max_val=None):
        while True:
            try:
                val = IntPrompt.ask(f"[bold white]{prompt}[/]")
                if (min_val is None or val >= min_val) and (max_val is None or val <= max_val):
                    return val
                console.print(f"[bold red]Value must be between {min_val} and {max_val}[/]")
            except:
                console.print("[bold red]Invalid input, please enter a valid number.[/]")

    def get_yes_no(self, prompt):
        return Confirm.ask(f"[bold white]{prompt}[/]")

    def get_choice(self, prompt, choices):
        console.print(f"[bold white]{prompt}[/]")
        for i, choice in enumerate(choices, 1):
            console.print(f"[yellow]{i}. {choice}[/]")
        while True:
            try:
                num = IntPrompt.ask("[bold white]Enter choice number[/]")
                if 1 <= num <= len(choices):
                    return choices[num - 1]
                console.print("[bold red]Invalid choice, please try again.[/]")
            except:
                console.print("[bold red]Invalid choice, please try again.[/]")

    def get_list(self, prompt):
        val = self.get_string(f"{prompt} (comma separated)")
        items = [item.strip() for item in val.split(",") if item.strip()]
        return items

    def get_key_value_pairs(self, prompt):
        console.print(f"[bold white]{prompt} (key=value, one per line. Empty line to finish)[/]")
        data = {}
        while True:
            key = self.get_string("key")
            if key == '':
                break
            value = self.get_string("value")
            data[key] = value
        return data

    def get_path_existing(self, prompt: str):
        """Prompt for a file path; accept quoted paths; ensure it exists."""
        while True:
            raw = self.get_string(prompt)
            path = raw.strip().strip('"').strip("'")
            path = os.path.expanduser(path)
            if os.path.isfile(path):
                return path
            console.print("[bold red]Invalid path, file not found. Please try again.[/]")

            