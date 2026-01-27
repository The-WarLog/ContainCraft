import yaml
from typing import Dict,Any

#first laod
def load_yaml(path:str)->Dict[str,Any]:
    with open(path,'r') as f:
        yaml_data=yaml.safe_load(f)
    return yaml_data
#then dump
def save_yaml(path:str,data:Dict[str,Any]):
    with open(path,'w') as f:
        yaml.safe_dump(data=data,stream=f,sort_keys=False,default_flow_style=False)
    