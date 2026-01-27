# schemas/docker_schema.py

from .base_schema import BaseSchema
from typing import Dict, Any,Literal
from ..ui.inputs import InputHandler
class DockerComposeSchema(BaseSchema):
    name = "docker-compose"
    #ui=InputHandler()
    def guide_user_input(self, ui:InputHandler) -> Dict[str, Any]:
        services = {}
        ui.print_header("Create Docker Compose YAML")

        while True:
            service_name = ui.get_string("Service name:")
            image = ui.get_string("Docker image (e.g., nginx:latest):")

            ports = ui.get_list("Ports (e.g., 8080:80), comma separated:")
            volumes = ui.get_list("Volumes (e.g., ./data:/var/lib/mysql):")
            env_vars = ui.get_key_value_pairs("Environment variables:")
            restart = ui.get_choice("Restart policy:", ["no", "always", "on-failure"])

            services[service_name] = {
                "image": image,
                "ports": ports if ports else [],
                "volumes": volumes if volumes else [],
                "environment": env_vars if env_vars else {},
                "restart": restart
            }

            if not ui.get_yes_no("Add another service?"):
                break

        return {"version": "3", "services": services}
    
    def validate(self, data) -> bool:
        if "services" not in data:
            raise ValueError("Missing 'services' key")
        return True

    def default_structure(self) -> Dict[str, Any]:
        return {"version": "3", "services": {}}
