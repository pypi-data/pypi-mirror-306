from langchain_core.runnables import RunnableConfig

from mtmai.core.logging import get_logger
from mtmai.models.graph_config import HomeChatState

logger = get_logger()


class HumanNode:
    def __init__(self):
        pass

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        logger.info("进入 human_node ")
        messages = state.messages
        user_input = state.user_input
        if user_input == "/1":
            logger.info("特殊指令1")

        return {
            # "messages": HumanMessage(content=user_input),
            "messages": [],
        }
