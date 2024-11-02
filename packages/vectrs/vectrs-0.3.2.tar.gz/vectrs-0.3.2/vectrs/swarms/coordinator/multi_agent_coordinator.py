from collections import defaultdict
from vectrs.networking.message_broker import MessageBroker
from vectrs.network import KademliaNode
import asyncio
import logging
from typing import Dict, Any, List
from vectrs.swarms.types import Agent, Response, Result
from vectrs.swarms.agent_factory import AgentFactory
from vectrs.swarms.knowledge_base.vector_db import VectorDB
from vectrs.swarms.llm.anthropic_llm import AnthropicLLM
from vectrs.swarms.utils.error_handler import ErrorHandler

logger = logging.getLogger(__name__)

class MultiAgentCoordinator:
    def __init__(self, message_broker: MessageBroker, node: KademliaNode, vector_db: VectorDB, llm: AnthropicLLM):
        self.agents = {}
        self.task_queue = asyncio.Queue()
        self.message_broker = message_broker
        self.node = node
        self.agent_factory = AgentFactory(self, vector_db, llm)
        self.vector_db = vector_db
        self.llm = llm
        
        # Create and register default agents
        self.create_and_register_default_agents()

    def create_and_register_default_agents(self):
        reflection_agent = self.agent_factory.create_agent("reflection", "reflection_agent")
        retrieval_agent = self.agent_factory.create_agent("retrieval", "retrieval_agent")
        tool_agent = self.agent_factory.create_agent("tool", "tool_agent")
        planning_agent = self.agent_factory.create_agent("planning", "planning_agent")
        generation_agent = self.agent_factory.create_agent("generation", "generation_agent")
        
        self.register_agent(reflection_agent)
        self.register_agent(retrieval_agent)
        self.register_agent(tool_agent)
        self.register_agent(planning_agent)
        self.register_agent(generation_agent)

    def register_agent(self, agent: Agent):
        self.agents[agent.agent_id] = agent
        self.message_broker.register_agent(agent.agent_id)

    async def add_task(self, task: Dict[str, Any]):
        await self.task_queue.put(task)

    async def process_tasks(self):
        while True:
            task = await self.task_queue.get()
            try:
                await self.assign_task(task)
            except Exception as e:
                await self.handle_error(e, {"task": task})
            finally:
                self.task_queue.task_done()

    async def assign_task(self, task: Dict[str, Any]):
        required_skills = self.identify_required_skills(task)
        suitable_agents = await self.find_suitable_agents(required_skills)
        if suitable_agents:
            selected_agent = max(suitable_agents, key=lambda a: a.capability_score(required_skills))
            try:
                result = await selected_agent.process_task(task)
                return self.handle_agent_result(result)
            except Exception as e:
                await self.handle_error(e, {"task": task, "agent": selected_agent.agent_id})
        else:
            logger.warning(f"No suitable agent found for task: {task}")
            # Fallback to using the LLM directly
            prompt = f"Please complete this task: {task['data']}"
            response = await self.llm.generate_text(prompt)
            return Result(value=response)

    async def find_suitable_agents(self, required_skills: set) -> List[Agent]:
        local_agents = [agent for agent in self.agents.values() if agent.has_required_skills(required_skills)]
        try:
            network_agents = await self.node.find_agents_with_skills(required_skills)
        except AttributeError:
            # If find_agents_with_skills is not implemented, just use local agents
            network_agents = []
        return local_agents + network_agents

    async def send_message(self, sender: str, recipient: str, message_type: str, content: Any):
        message = {
            'sender': sender,
            'recipient': recipient,
            'type': message_type,
            'content': content
        }
        await self.message_broker.send_message(message)

    async def deliver_messages(self):
        while True:
            for agent_id, agent in self.agents.items():
                messages = await self.message_broker.get_messages(agent_id)
                for message in messages:
                    await agent.receive_message(message)
            await asyncio.sleep(0.1)  # Avoid busy-waiting

    async def run(self):
        await asyncio.gather(
            self.process_tasks(),
            self.deliver_messages()
        )

    def identify_required_skills(self, task: Dict[str, Any]) -> set:
        skills = set()
        if 'type' in task:
            if task['type'] == 'reflection':
                skills.add('self-evaluation')
            elif task['type'] == 'retrieval':
                skills.add('information_retrieval')
            elif task['type'] == 'planning':
                skills.add('task_planning')
            elif task['type'] == 'generation':
                skills.add('text_generation')
            elif task['type'] == 'tool_usage':
                skills.add('tool_usage')
        return skills

    async def handle_error(self, error: Exception, context: dict):
        error_type = type(error).__name__
        error_message = str(error)
        
        logger.error(f"Error occurred: {error_type} - {error_message}")
        logger.error(f"Context: {context}")
        
        if isinstance(error, ValueError):
            logger.info("Attempting to recover from ValueError...")
            # Implement recovery logic here
        elif isinstance(error, TimeoutError):
            logger.info("Attempting to retry after TimeoutError...")
            # Implement retry logic here
        else:
            logger.warning("Unhandled error type. Propagating error...")
            raise error

    def handle_agent_result(self, result: Any) -> Result:
        if isinstance(result, Result):
            return result
        elif isinstance(result, Agent):
            return Result(value=result.agent_id, agent=result)
        else:
            try:
                return Result(value=str(result))
            except Exception as e:
                error_message = f"Failed to cast response to string: {result}. Make sure agent functions return a string or Result object. Error: {str(e)}"
                logger.error(error_message)
                raise TypeError(error_message)

    async def run_rag_workflow(self, query: str) -> Dict[str, Any]:
        logger.info(f"Starting RAG workflow for query: {query}")
        
        try:
            # Step 1: Retrieval
            retrieval_task = {'type': 'retrieval', 'data': f"Retrieve relevant information for the query: {query}"}
            retrieval_result = await self.assign_task(retrieval_task)
            
            # Step 2: Planning
            planning_task = {'type': 'planning', 'data': f"Create a detailed plan to answer the query: {query}\nContext: {retrieval_result.value}"}
            plan = await self.assign_task(planning_task)
            
            # Step 3: Generation
            generation_task = {'type': 'generation', 'data': f"Generate an answer to the query: {query}\nContext: {retrieval_result.value}\nPlan: {plan.value}"}
            generation_result = await self.assign_task(generation_task)
            
            # Step 4: Reflection
            reflection_task = {'type': 'reflection', 'data': f"Reflect on and improve the generated answer: {generation_result.value}"}
            reflection = await self.assign_task(reflection_task)
            
            final_result = {
                'query': query,
                'retrieved_context': retrieval_result.value,
                'plan': plan.value,
                'generated_answer': generation_result.value,
                'reflection': reflection.value
            }
            
            logger.info(f"RAG workflow completed. Final result: {final_result}")
            return final_result
        except Exception as e:
            logger.error(f"Error in RAG workflow: {str(e)}")
            return await ErrorHandler.handle_error(e, {"query": query})

    async def create_agent(self, agent_type: str, agent_id: str, **kwargs):
        agent = self.agent_factory.create_agent(agent_type, agent_id, **kwargs)
        self.register_agent(agent)
        return agent
