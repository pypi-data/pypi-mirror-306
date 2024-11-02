from typing import List, Callable, Union, Optional, Dict, Any
from pydantic import BaseModel

class Agent(BaseModel):
    agent_id: str
    skills: set
    model: str
    instructions: Union[str, Callable[[], str]]

    def has_required_skills(self, required_skills: set) -> bool:
        return self.skills.issuperset(required_skills)

    def capability_score(self, required_skills: set) -> float:
        return len(self.skills.intersection(required_skills)) / len(required_skills)

class Result(BaseModel):
    value: Union[str, Dict[str, Any]]
    agent: Optional[Agent] = None
    context_variables: dict = {}

class Response(BaseModel):
    messages: List = []
    agent: Optional[Agent] = None
    context_variables: dict = {}

# ... rest of the file remains the same

