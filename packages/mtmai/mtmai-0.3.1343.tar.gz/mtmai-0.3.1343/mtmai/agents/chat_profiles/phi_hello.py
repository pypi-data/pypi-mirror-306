from phi.agent import AgentMemory
from rich.pretty import pprint

import mtmai.chainlit as cl
from mtmai.agents.phiagents.workbrench_agent import workbrench_agent
from mtmai.chainlit import context
from mtmai.core.logging import get_logger
from mtmai.models.chat import ChatProfile

logger = get_logger()


class PhiHelloAgent:
    @classmethod
    def name(cls):
        return "PhiHelloAgent"

    @classmethod
    def get_chat_profile(self):
        return ChatProfile(
            name="PhiHelloAgent",
            description="Phi Hello Agent",
        )

    async def chat_start(self):
        user_session = cl.user_session
        thread_id = context.session.thread_id
        # await cl.Message(content="Phi Hello Agent").send()

    async def on_message(self, message: cl.Message):
        await self.run_phi_assistant(message)

    async def run_phi_assistant(self, message: cl.Message):
        rsp_msg = cl.Message(content="")
        await rsp_msg.send()

        rsp = await workbrench_agent.arun(message.content, stream=True)
        async for items in rsp:
            logger.info(
                "e: %s, ct: %s, c: %s",
                items.event,
                items.content_type,
                items.content,
            )
            await rsp_msg.stream_token(items.content)

        memory: AgentMemory = workbrench_agent.memory

        await rsp_msg.send()
        # -*- Print Chats
        print("============ Chats ============")
        pprint(memory.chats)

        # -*- Print messages
        print("============ Messages ============")
        pprint(memory.messages)
