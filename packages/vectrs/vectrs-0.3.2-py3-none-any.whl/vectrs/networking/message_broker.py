from vectrs.network import KademliaNode
from typing import Dict, Any, List
import asyncio

class MessageBroker:
    def __init__(self, node: KademliaNode):
        self.node = node
        self.message_queues = {}

    def register_agent(self, agent_id: str):
        self.message_queues[agent_id] = asyncio.Queue()

    async def send_message(self, message: Dict[str, Any]):
        recipient = message['recipient']
        if recipient in self.message_queues:
            await self.message_queues[recipient].put(message)
        else:
            # If the recipient is not local, store the message in the distributed network
            await self.node.set_value(f"message:{recipient}", message)

    async def get_messages(self, agent_id: str) -> List[Dict[str, Any]]:
        messages = []
        while not self.message_queues[agent_id].empty():
            messages.append(await self.message_queues[agent_id].get())
        
        # Also check for messages in the distributed network
        network_messages = await self.node.get_value(f"message:{agent_id}")
        if network_messages:
            messages.extend(network_messages)
            await self.node.delete_value(f"message:{agent_id}")
        
        return messages