from anthropic import Anthropic
from .llm_interface import LLMInterface
from typing import List, Union
from sentence_transformers import SentenceTransformer
import numpy as np
import asyncio

class AnthropicLLM(LLMInterface):
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    async def generate_text(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        message = await loop.run_in_executor(None, lambda: self.client.messages.create(
            model="claude-2.1",
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        ))
        return message.content

    async def embed_text(self, text: Union[str, object]) -> List[float]:
        loop = asyncio.get_event_loop()
        # Convert TextBlock or any other object to string
        if not isinstance(text, str):
            text = str(text)
        embedding = await loop.run_in_executor(None, lambda: self.model.encode([text])[0].tolist())
        return embedding

    def adjust_embedding_dimension(self, embedding: List[float], target_dim: int) -> List[float]:
        current_dim = len(embedding)
        if current_dim < target_dim:
            return np.pad(embedding, (0, target_dim - current_dim), 'constant').tolist()
        elif current_dim > target_dim:
            return embedding[:target_dim]
        return embedding
