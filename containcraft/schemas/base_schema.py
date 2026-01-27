
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseSchema(ABC):
    name = "base"

    @abstractmethod
    def guide_user_input(self, ui) -> Dict[str, Any]:
        pass

    @abstractmethod
    def validate(self, data) -> bool:
        return True

    @abstractmethod
    def default_structure(self) -> Dict[str, Any]:
        return {}
