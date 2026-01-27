# schemas/k8s_schema.py

from .base_schema import BaseSchema
from typing import Dict, Any
from ..ui.inputs import InputHandler
class KubernetesSchema(BaseSchema):
    name = "kubernetes"

    def guide_user_input(self, ui:InputHandler) -> Dict[str, Any]:
        ui.print_header("Create Kubernetes YAML")

        kind = ui.get_choice("Resource kind:", ["Deployment", "Service"])
        name = ui.get_string("Metadata name:")
        labels = ui.get_key_value_pairs("Labels:")

        if kind == "Deployment":
            replicas = ui.get_number("Replicas:", min_val=1)
            container_name = ui.get_string("Container name:")
            image = ui.get_string("Image:")
            ports = ui.get_list("Container ports (80,443):")
            env_vars = ui.get_key_value_pairs("Environment variables:")

            return {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {
                    "name": name,
                    "labels": labels
                },
                "spec": {
                    "replicas": replicas,
                    "selector": {
                        "matchLabels": labels
                    },
                    "template": {
                        "metadata": {"labels": labels},
                        "spec": {
                            "containers": [{
                                "name": container_name,
                                "image": image,
                                "ports": [{"containerPort": int(p)} for p in ports],
                                "env": [{"name": k, "value": v} for k, v in env_vars.items()]
                            }]
                        }
                    }
                }
            }

        if kind == "Service":
            service_type = ui.get_choice("Service type:", ["ClusterIP", "NodePort", "LoadBalancer"])
            ports = ui.get_list("Ports (80:80, 443:443):")

            return {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "name": name,
                    "labels": labels
                },
                "spec": {
                    "type": service_type,
                    "selector": labels,
                    "ports": [
                        {
                            "port": int(p.split(":")[1]),
                            "targetPort": int(p.split(":")[0])
                        } for p in ports
                    ]
                }
            }
        return {}

    def validate(self, data) -> bool:
        if "apiVersion" not in data:
            raise ValueError("Missing 'apiVersion' key")
        return True

    def default_structure(self) -> Dict[str, Any]:
        return {}
