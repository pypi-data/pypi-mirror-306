from urllib.parse import urlparse

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from mtmai.agents.ctx import init_mtmai_http_context
from mtmai.agents.task_graph.task_state import TaskState
from mtmai.chainlit import context as clctx
from mtmai.db.db import get_async_session
from mtmai.core.logging import get_logger
from mtmai.crud import crud_task
from mtmai.models.task import MtTaskType

logger = get_logger()


def routeEntryPath(state: TaskState):
    # is_tools = tools_condition(state)
    # if is_tools == "tools":
    #     return "chat_tools_node"
    if not state.next:
        raise ValueError("state.next not set")
    return state.next


class TaskEntryNode:
    def __init__(self):
        pass

    async def __call__(self, state: TaskState, config: RunnableConfig):
        logger.info(f"task entry node: {state}")
        init_mtmai_http_context()
        if not state.scheduleId:
            scheduleId = await self.detect_client_info()
            state.scheduleId = scheduleId
        if not scheduleId:
            return {
                "next": "assistant",
                "human_ouput_message": "未找到 任务配置",
            }
        async with get_async_session() as session:
            sched = await crud_task.get_schedule(session=session, id=state.scheduleId)

        # 判断任务类型
        task_type = sched.task_type
        if task_type == MtTaskType.ARTICLE_GEN:
            logger.info("是文章生成任务")
            return {
                "next": "articleGen",
            }
        else:
            logger.info("未知的任务类型")
            return {
                "next": "assistant",
                "human_ouput_message": "未知的任务类型",
            }
        task_params = sched.params
        if state.user_input:
            return {
                "next": "assistant",
                "messages": [HumanMessage(content=state.user_input)],
            }
        return {
            "next": "assistant",
        }

    async def detect_client_info(self):
        """
        通过函数js 函数获取客户端的基本信息
        """
        js_code_get_detail_info = """
var results = {};
results.fullUrl=window.location.href;
results.cookie=document.cookie;
results.title=document.title;
results.body=document.body.innerText;
(function() { return results; })();
"""
        js_eval_result = await clctx.emitter.send_call_fn(
            "js_eval", {"code": js_code_get_detail_info}
        )
        logger.info("js_eval_result %s", js_eval_result)

        client_url = js_eval_result.get("fullUrl")
        logger.info("client_url %s", client_url)

        # Parse the URL to extract scheduleId and taskId

        parsed_url = urlparse(client_url)
        path_segments = parsed_url.path.split("/")

        scheduleId = None
        # taskId = None

        if len(path_segments) >= 3 and path_segments[2] == "chat-profile":
            scheduleId = path_segments[3]

        # if len(path_segments) >= 7 and path_segments[5] == "task":
        #     taskId = path_segments[6]

        # logger.info(f"Extracted scheduleId: {scheduleId}, taskId: {taskId}")

        # Store the extracted IDs in the user session for later use
        # cl.user_session.set("scheduleId", scheduleId)
        # cl.user_session.set("taskId", taskId)
        return scheduleId
