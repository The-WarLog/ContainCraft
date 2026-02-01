from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Prompt
from ..schemas.docker_schema import DockerComposeSchema
from ..schemas.custom_schema import CustomSchema
from ..schemas.k8s_schema import KubernetesSchema
from ..schemas.kafka_schema import KafkaSchema
from ..schemas.base_schema import BaseSchema
from ..edit.edit_yaml import edit_yaml_session
from .inputs import InputHandler

from ..core.json_model import JSONModel
from ..core.renderer import render_tree
from ..core.yaml_tree import YamlTree
from ..core.yaml_io import load_yaml, save_yaml
from ..core.json_converter import (
    json_to_yaml,
    yaml_to_json,
    preview_json_to_yaml,
    preview_yaml_to_json,
    display_preview
)
from typing import Dict
import yaml
import os
from pathlib import Path
console = Console()

class Menu:
    def __init__(self) -> None:
        self.ui: InputHandler = InputHandler()
        self.schemas: Dict[str, BaseSchema] = {
            "Docker Compose":DockerComposeSchema(),
            "Kubernetes":KubernetesSchema(),
            "Kafka Configuration":KafkaSchema(),
            "Custom":CustomSchema()
        }
    def main_menu(self):
        while True:
            console.clear()
            console.print(Panel("ContainCraft — YAML Builder", style="bold green", expand=False))
            console.print()
            choice = self.ui.get_choice(
                "Select an option:",
                ["Create new YAML",
                 "Load existing YAML",
                 "Edit YAML",
                 "Convert Files (JSON ↔ YAML)",
                 "Exit"]
            )
            if choice == "Create new YAML":
                self.create_yaml_flow()
            elif choice == "Load existing YAML":
                self.load_yaml_flow()
            elif choice == "Edit YAML":
                self.edit_yaml_flow()
            elif choice == "Convert Files (JSON ↔ YAML)":
                self.conversion_menu()
            elif choice == "Exit":
                console.print("[bold yellow]Exiting ContainCraft. Goodbye![/]")
                break
    '''create new yaml'''
    def create_yaml_flow(self):
        schema_name = self.ui.get_choice("Choose schema type:", list(self.schemas.keys()))
        schema: BaseSchema = self.schemas[schema_name]

        data = schema.guide_user_input(self.ui)
        schema.validate(data)

        file_path = self.ui.get_string("Enter the filename (filename.yaml)")
        if not file_path.endswith(('.yaml', '.yml')):
            file_path += '.yaml'
        file_path_directory=Prompt.ask("[bold white]Enter directory to save file (leave blank for current directory)[/]").strip()
        if file_path_directory:
            Path(file_path_directory).mkdir(parents=True,exist_ok=True)
            os.path.join(file_path_directory,file_path)

        
        save_yaml(file_path, data)

        console.print(f"[bold green]✓ Saved to {file_path}[/]")
        input("Press Enter to continue...")

    #  load YAML 

    def load_yaml_flow(self):
        file_path = self.ui.get_path_existing("Enter YAML file path or press enter to go back to main menu")
        # User pressed Enter to go back to main menu
        if file_path is None:
            return
        
        data = load_yaml(file_path)
        # If data is None, file couldn't be loaded
        if data is None:
            console.print("[bold red]Error: Could not load YAML file[/]")
            input("Press Enter to continue...")
            return

        console.print("\n[bold cyan]Loaded YAML:[/]\n")
        yaml_str = yaml.safe_dump(data, sort_keys=False, default_flow_style=False)
        console.print(Panel(Syntax(yaml_str, "yaml", theme="monokai"), title="YAML Content", border_style="cyan"))

        tree = YamlTree()
        tree.load_from_dict(data)
        if tree.root is None:
            console.print("[bold red]Error: Could not build tree from YAML[/]")
            input("Press Enter to continue...")
            return

        console.print("\n[bold blue]Tree View:[/]\n")
        console.print(Panel(render_tree(tree.root), border_style="blue", title="Tree Structure"))
        #return data,file_path
        input("\nPress Enter to continue..." )
        
    def edit_yaml_flow(self):
        file_path=self.ui.get_path_existing("Enter YAML file path to edit")
        data=load_yaml(file_path)
        result=edit_yaml_session(data)
        if result is not None:
            save_yaml(file_path,result)
            console.print(f"[bold green]✓ Changes saved to {file_path}[/]")
            input("Press Enter to continue...")
       



    def _pretty_yaml_box(self, data) -> str:
        dumped = yaml.safe_dump(data, sort_keys=False, default_flow_style=False)
        return dumped

    def conversion_menu(self):
        """Handle file conversion between JSON and YAML formats."""
        while True:
            console.clear()
            console.print(Panel("File Conversion — JSON ↔ YAML", style="bold cyan", expand=False))
            console.print()
            
            choice = self.ui.get_choice(
                "Select conversion type:",
                ["JSON → YAML",
                 "YAML → JSON",
                 "Back to Main Menu"]
            )
            
            if choice == "JSON → YAML":
                self.json_to_yaml_flow()
            elif choice == "YAML → JSON":
                self.yaml_to_json_flow()
            elif choice == "Back to Main Menu":
                break

    def json_to_yaml_flow(self):
        """Convert JSON file to YAML with preview."""
        console.print("\n[bold cyan]JSON → YAML Conversion[/]\n")
        
        # Get source JSON file
        json_path = self.ui.get_path_existing("Enter JSON file path")
        if json_path is None:
            return
        
        if not json_path.endswith('.json'):
            console.print("[bold yellow]Warning: File doesn't have .json extension[/]")
        
        # Generate preview
        console.print("\n[bold yellow]Generating preview...[/]\n")
        preview = preview_json_to_yaml(json_path)
        
        if preview is None:
            console.print("[bold red]Failed to generate preview[/]")
            input("Press Enter to continue...")
            return
        
        # Display preview
        display_preview(preview, "yaml", "YAML Preview")
        
        # Confirm conversion
        if not self.ui.get_yes_no("\nProceed with conversion?"):
            console.print("[yellow]Conversion cancelled[/]")
            input("Press Enter to continue...")
            return
        
        # Get output path
        yaml_path = self.ui.get_string("Enter output YAML file path")
        if not yaml_path.endswith(('.yaml', '.yml')):
            yaml_path += '.yaml'
        
        # Perform conversion
        if json_to_yaml(json_path, yaml_path):
            console.print(f"[bold green]✓ Conversion complete![/]")
        else:
            console.print("[bold red]✗ Conversion failed[/]")
        
        input("\nPress Enter to continue...")

    def yaml_to_json_flow(self):
        """Convert YAML file to JSON with preview."""
        console.print("\n[bold cyan]YAML → JSON Conversion[/]\n")
        
        # Get source YAML file
        yaml_path = self.ui.get_path_existing("Enter YAML file path")
        if yaml_path is None:
            return
        
        if not yaml_path.endswith(('.yaml', '.yml')):
            console.print("[bold yellow]Warning: File doesn't have .yaml/.yml extension[/]")
        
        # Generate preview
        console.print("\n[bold yellow]Generating preview...[/]\n")
        preview = preview_yaml_to_json(yaml_path)
        
        if preview is None:
            console.print("[bold red]Failed to generate preview[/]")
            input("Press Enter to continue...")
            return
        
        # Display preview
        display_preview(preview, "json", "JSON Preview")
        
        # Confirm conversion
        if not self.ui.get_yes_no("\nProceed with conversion?"):
            console.print("[yellow]Conversion cancelled[/]")
            input("Press Enter to continue...")
            return
        
        # Get output path
        json_path = self.ui.get_string("Enter output JSON file path")
        if not json_path.endswith('.json'):
            json_path += '.json'
        
        # Perform conversion
        if yaml_to_json(yaml_path, json_path):
            console.print(f"[bold green]✓ Conversion complete![/]")
        else:
            console.print("[bold red]✗ Conversion failed[/]")
        
        input("\nPress Enter to continue...")