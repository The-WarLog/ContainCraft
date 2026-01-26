# schemas/kafka_schema.py

from .base_schema import BaseSchema
from typing import Annotated,Any, Literal,Dict
from ui.inputs import InputHandler
class KafkaSchema(BaseSchema):
    name = "kafka"

    def guide_user_input(self, ui:InputHandler)->Dict[str,Any]:
        ui.print_header("Create Kafka YAML")

        brokers = {}

        num_brokers = ui.get_number("Number of brokers:", min_val=1)

        for i in range(num_brokers):
            ui.print_header(f"Broker {i+1}")

            broker_id = ui.get_number("Broker ID:", min_val=0)
            port = ui.get_number("Listener port:", min_val=1)
            log_dir = ui.get_string("Log directory (e.g., /kafka/logs):")
            env_vars = ui.get_key_value_pairs("Environment vars:")

            brokers[f"broker-{i+1}"] = {
                "broker.id": broker_id,
                "listeners": f"PLAINTEXT://:{port}",
                "log.dirs": log_dir,
                "environment": env_vars,
            }

        zookeeper = ui.get_string("Zookeeper host (e.g., zookeeper:2181):")

        return {
            "cluster": {
                "zookeeper": zookeeper,
                "brokers": brokers
            }
        }

    def validate(self, data)->bool:
        return "cluster" in data and "brokers" in data["cluster"]

    def default_structure(self)->Dict[str,Any]:
        return {"cluster": {"zookeeper": "", "brokers": {}}}
