from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Prompt
from schemas.docker_schema import DockerComposeSchema
from schemas.custom_schema import CustomSchema
from schemas.k8s_schema import KubernetesSchema
from schemas.kafka_schema import KafkaSchema
from schemas.base_schema import BaseSchema
from edit.edit_yaml import edit_yaml_session
from ui.inputs import InputHandler

from core.json_model import JSONModel
from core.renderer import render_tree
from core.yaml_tree import YamlTree
from core.yaml_io import load_yaml, save_yaml
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
                 "Exit"]
            )
            if choice == "Create new YAML":
                self.create_yaml_flow()
            elif choice == "Load existing YAML":
                self.load_yaml_flow()
            elif choice == "Edit YAML":
                self.edit_yaml_flow()
                
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
        file_path = self.ui.get_path_existing("Enter YAML file path")
        data = load_yaml(file_path)

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