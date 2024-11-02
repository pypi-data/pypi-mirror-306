from abc import ABC, abstractmethod
from typing import List

class LLMInterface(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str) -> str:
        pass

    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        pass
