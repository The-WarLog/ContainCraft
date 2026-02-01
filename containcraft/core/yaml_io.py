import yaml
import json
from typing import Dict,Any

def load_yaml(path:str | None)->Dict[str,Any] | None:
    """Load YAML file and return as dictionary."""
    yaml_data=None
    if path is not None and path!="":
        with open(path,'r') as f:
            yaml_data=yaml.safe_load(f)
    return yaml_data

def save_yaml(path:str | None,data:Dict[str,Any] | None)->None:
    """Save dictionary as YAML file."""
    if path is not None and path!="":
        with open(path,'w') as f:
            yaml.safe_dump(data=data,stream=f,sort_keys=False,default_flow_style=False)

def load_json(path: str | None) -> Dict[str, Any] | None:
    """Load JSON file and return as dictionary."""
    json_data = None
    if path is not None and path != "":
        with open(path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    return json_data


def save_json(path: str | None, data: Dict[str, Any] | None, indent: int = 2, sort_keys: bool = False) -> None:
    """Save dictionary as JSON file."""
    if path is not None and path != "":
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, sort_keys=sort_keys, ensure_ascii=False)