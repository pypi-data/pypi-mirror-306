import uuid
from typing import Any
from urllib.parse import uses_query

from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlmodel import func, select

from mtmai.biz import biz_scheule
from mtmai.core.event import emit_flow_event
from mtmai.core.logging import get_logger
from mtmai.crud import crud_sysitem, crud_task, curd
from mtmai.deps import AsyncSessionDep, CurrentUser, OptionalUserDep
from mtmai.models.base_model import CommonResultResponse, ListResponse
from mtmai.models.task import (
    MtTask,
    MtTaskStatus,
    ScheduleCreateRequest,
    ScheduleCreateResponse,
    ScheduleDetailPublic,
    ScheduleListRequest,
    ScheduleUpdateRequest,
    ScheduleUpdateResponse,
    SiteAutoItemPublic,
    TaskListResponse,
)

from datetime import datetime

from fastapi.responses import StreamingResponse
import structlog
from fastapi import APIRouter, HTTPException, Request, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from websockets.exceptions import ConnectionClosedOK

from mtmai.forge import app
from mtmai.forge.sdk.schemas import organizations
from mtmai.forge.sdk.schemas.tasks import CreateTaskResponse, TaskStatus
from mtmai.forge.sdk.services.org_auth_service import get_current_org
from mtmai.forge.sdk.workflow.models.workflow import WorkflowRunStatus
from mtmai.mtlibs import aisdk
from mtmai.mtlibs.aiutils import stream_text
from mtmtrain.__main__ import task_a
from pydantic import BaseModel

LOG = structlog.get_logger()
websocket_router = APIRouter()
STREAMING_TIMEOUT = 300

router = APIRouter()
logger = get_logger()


class TaskListRequest(BaseModel):
    query: str = Query(default="")
    siteId: str | None = None
    skip: int = 0
    limit: int = Query(default=100, le=100)


@router.post("/tasks", response_model=TaskListResponse)
async def task_list(
    *,
    session: AsyncSessionDep,
    user: CurrentUser,
    req: TaskListRequest,
):
    base_query = select(MtTask)
    count_query = select(func.count()).select_from(MtTask)

    if not user.is_superuser:
        base_query = base_query.where(MtTask.owner_id == user.id)
        count_query = count_query.where(MtTask.owner_id == user.id)

    if req.siteId:
        base_query = uses_query.where(MtTask.site_id == req.siteId)
        count_query = count_query.where(MtTask.site_id == req.siteId)

    count = session.exec(count_query).one()

    statement = base_query.offset(req.skip).limit(req.limit)
    items = session.exec(statement).all()

    return TaskListResponse(data=items, count=count)


@router.get("/{mttask_id}", response_model=MtTask)
async def get_mttask(
    *,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    mttask_id: str,
):
    """
    Get task by id.
    """
    item = await crud_task.mttask_get_by_id(session=session, mttask_id=mttask_id)
    if not item or item.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="not found")
    return item


class DrowndownSelectItem(BaseModel):
    id: str
    value: str
    title: str
    description: str


class SelectItemsResponse(BaseModel):
    items: list[DrowndownSelectItem]
    count: int


@router.post("/task_types", response_model=SelectItemsResponse)
async def task_types(
    *,
    session: AsyncSessionDep,
    current_user: CurrentUser,
):
    """
    Get task types.
    """

    sysitems = await crud_sysitem.get_sys_items(session=session, type="task_type")
    if sysitems:
        items = []
        for sysitem in sysitems:
            items.append(
                DrowndownSelectItem(
                    id=sysitem.key,
                    title=sysitem.description,
                    description=sysitem.description,
                    value=sysitem.value,
                )
            )
        return SelectItemsResponse(items=items, count=len(items))

    raise HTTPException(status_code=404, detail="Task types not found")


class MttaskUpdateStatusRequest(BaseModel):
    mttask_id: str
    status: str


@router.post("/mttask_update_status", response_model=CommonResultResponse)
async def mttask_update_status(
    *,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    item_in: MttaskUpdateStatusRequest,
):
    """
    更新任务状态
    """
    mttask = await crud_task.mttask_get_by_id(
        session=session, mttask_id=item_in.mttask_id
    )
    if not mttask:
        raise HTTPException(status_code=404, detail="not found")
    if mttask.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="forbidden")

    # 状态对比
    if mttask.status == item_in.status:
        return CommonResultResponse(
            data={"status": "success"}, message="更新任务状态成功"
        )

    # 如果状态不一样
    if mttask.status == MtTaskStatus.NEW:
        if item_in.status == "pending":
            event_result = await emit_flow_event(
                event="mtmai.mttask.update_status",
                resource_id=str(mttask.id),
                # data={"mttask_id": str(mttask.id)},
            )
            logger.info(event_result)
    if mttask.status == "pending":
        if item_in.status == "running":
            await emit_flow_event(
                event="mtmai.mttask.update_status",
                resource_id=str(mttask.id),
                # data={"mttask_id": str(mttask.id)},
            )
            session.add(mttask)
            await session.commit()
            return CommonResultResponse(
                data={"status": "success"}, message="更新任务状态成功"
            )

        elif item_in.status == "success":
            pass
        elif item_in.status == "failed":
            pass
        # else:
        #     raise HTTPException(status_code=400, detail="invalid status")
    # await crud_task.mttask_update_state(
    #     session=session, mttask_id=item_in.mttask_id, status=item_in.status
    # )
    raise HTTPException(status_code=400, detail="invalid status")


@router.get("/schedule/{id}", response_model=ScheduleDetailPublic)
async def schedule_get(
    *,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    id: str,
) -> Any:
    try:
        return await crud_task.get_schedule(session, id, current_user.id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="not found")


@router.post("/schedule/list", response_model=ListResponse[SiteAutoItemPublic])
async def schedule_list(
    session: AsyncSessionDep,
    current_user: OptionalUserDep,
    req: ScheduleListRequest,
):
    """
    Retrieve site auto items with pagination.
    """
    items, count = await crud_task.list_schedule(session, req, current_user.id)

    return ListResponse(items=jsonable_encoder(items), count=count)


@router.post("/schedule/create", response_model=ScheduleCreateResponse)
async def schedule_create(
    *,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    req: ScheduleCreateRequest,
) -> Any:
    return await crud_task.create_schedule(session, req, user_id=current_user.id)


@router.put("/schedule/update/{id}", response_model=ScheduleUpdateResponse)
async def schedule_update(
    *,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    id: str,
    item_in: ScheduleUpdateRequest,
) -> Any:
    item_in.id = uuid.UUID(id)
    update_result = await crud_task.update_schedule(session, item_in, current_user.id)
    return update_result


# @router.post("/schedule/{schedule_id}/new_task", response_model=TaskCreateResponse)
# async def new_task(
#     *,
#     session: AsyncSessionDep,
#     current_user: CurrentUser,
#     schedule_id: str,
#     req: TaskCreateRequest,
# ):
#     """根据调度配置，立即生成一个运行任务"""
#     new_task = await biz_scheule.make_new_task_by_schedule(schedule_id, req.is_auto)
#     return new_task


@router.delete("/chat_profile/{id}", response_model=CommonResultResponse)
async def cht_profile_delete(
    *,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    id: str,
):
    """根据调度配置，立即生成一个运行任务"""
    new_task = await biz_scheule.delete_chat_profile(id)
    return new_task


LOG = structlog.get_logger()

class TaskArtifact(BaseModel):
    artifact_type: str
    artifact_data: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: TaskStatus
    artifact: TaskArtifact | None = None

class TaskStatusRequest(BaseModel):
    task_id: str

@router.post("/task_status_v2", response_model=TaskStatusResponse)
async def status_v2(
    req: TaskStatusRequest,
    current_user: CurrentUser,
    apikey: str | None = None,
    token: str | None = None,
):
    """
    Get the status of a task, 专用于 TaskActions 界面中的状态沦陷（放弃websocket形式）
    """
    try:
        # organization = await get_current_org(x_api_key=apikey, authorization=token)
        org = await curd.get_organization_by_user_id(current_user.id)
        organization_id = org.organization_id
    except Exception:
        LOG.exception("Error while getting organization", task_id=task_a)
        try:
            raise HTTPException(status_code=401, detail="Invalid credential provided")
        except ConnectionClosedOK:
            LOG.info(
                "ConnectionClosedOK error while sending invalid credential message"
            )
        return

    task = await app.DATABASE.get_task(
                task_id=req.task_id, organization_id=organization_id
            )
    return TaskStatusResponse(
        task_id=task.task_id,
        status=task.status,
        # artifact=task.artifact,
    )
