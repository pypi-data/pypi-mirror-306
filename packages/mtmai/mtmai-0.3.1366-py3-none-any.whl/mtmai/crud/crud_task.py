import json
import uuid

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlmodel import delete, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.crud.curd_search import generate_search_vector
from mtmai.models.search_index import SearchIndex
from mtmai.models.site import Site
from mtmai.models.task import (
    MtTask,
    ScheduleCreateRequest,
    ScheduleListRequest,
    ScheduleUpdateRequest,
    TaskCreateRequest,
    # TaskCreateRequest,
    TaskSchedule,
)


async def create_task(
    *, session: AsyncSession, task_create: TaskCreateRequest, owner_id: str | uuid.UUID
):
    if isinstance(owner_id, str):
        owner_id = uuid.UUID(owner_id)
    db_item = MtTask(
        name=task_create.taskType,
        site_id=task_create.siteId,
        owner_id=owner_id,
        status="pending",
        description="",
        state={},
        priority=3,
    )
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    await mttask_search_index(session, db_item)
    await session.refresh(db_item)
    return db_item


async def mttask_search_index(session: AsyncSession, mttask: MtTask):
    if not mttask.title:
        mttask.title = "no title task"
    if not mttask.description:
        mttask.description = ""
    content_summary = (
        mttask.title + " " + mttask.description + " " + json.dumps(mttask.payload)
    )
    search_index = SearchIndex(
        content_type="mttask",
        content_id=mttask.id,
        title=mttask.title or "no_title",
        owner_id=mttask.owner_id,
        content_summary=content_summary,
        meta={},
        search_vector=await generate_search_vector(session, content_summary),
    )
    session.add(search_index)
    await session.commit()
    await session.refresh(search_index)


async def get_tasks_to_run(*, session: AsyncSession, site_id: str | uuid.UUID, limit=1):
    """获取一个需要运行的任务"""
    if isinstance(site_id, str):
        site_id = uuid.UUID(site_id)

    statement = (
        select(MtTask)
        .where(MtTask.status == "pending", MtTask.site_id == site_id)
        .order_by(MtTask.priority.desc())
        .limit(limit)
    )
    result = await session.exec(statement)
    return result.all()


async def mttask_get_by_id(*, session: AsyncSession, mttask_id: str | uuid.UUID):
    """根据 id 获取一个任务"""
    if isinstance(mttask_id, str):
        mttask_id = uuid.UUID(mttask_id)
    statement = select(MtTask).where(MtTask.id == mttask_id)
    result = await session.exec(statement)
    return result.first()


async def mttask_update_state(
    *, session: AsyncSession, mttask_id: str | uuid.UUID, state: dict
):
    """更新任务 state"""
    if isinstance(mttask_id, str):
        mttask_id = uuid.UUID(mttask_id)
    statement = select(MtTask).where(MtTask.id == mttask_id)
    result = await session.exec(statement)
    db_item = result.first()
    if db_item:
        db_item.state = jsonable_encoder(state)
        await session.commit()
        await session.refresh(db_item)


async def mttask_create(
    *,
    session: AsyncSession,
    schedule_id: uuid.UUID | str,
    name=str,
    init_state: dict = {},
):
    if not name:
        raise ValueError("mttask_create name is required")
    if isinstance(schedule_id, str):
        schedule_id = uuid.UUID(schedule_id)

    schedule = await get_schedule(session=session, id=schedule_id)
    if not schedule:
        raise ValueError("mttask_create schedule_id not found")
    new_mttask = MtTask(
        name=name,
        # site_id=schedule.site_id,
        schedule_id=schedule_id,
        owner_id=schedule.owner_id,
        status="pending",
        state=init_state,
        priority=3,
    )
    session.add(new_mttask)
    await session.commit()
    await session.refresh(new_mttask)
    return new_mttask


async def get_schedule(
    session: AsyncSession,
    id: uuid.UUID | str,
    user_id: uuid.UUID | str | None = None,
):
    if isinstance(id, str):
        id = uuid.UUID(id)

    statement = select(TaskSchedule).where(TaskSchedule.id == id)

    if user_id:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        statement = statement.where(TaskSchedule.owner_id == user_id)

    result = await session.exec(statement)
    return result.one_or_none()


async def delete_chat_profile(
    session: AsyncSession,
    id: uuid.UUID | str,
    user_id: uuid.UUID | str | None = None,
):
    if isinstance(id, str):
        id = uuid.UUID(id)

    statement = delete(TaskSchedule).where(TaskSchedule.id == id)

    if user_id:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        statement = statement.where(TaskSchedule.owner_id == user_id)

    result = await session.exec(statement)
    await session.commit()
    return result.rowcount > 0


async def list_schedule(
    session: AsyncSession,
    req: ScheduleListRequest,
    user_id: uuid.UUID | str | None,
):
    """获取任务调度"""
    if isinstance(user_id, str):
        user_id = uuid.UUID(user_id)
    base_query = select(TaskSchedule)
    if user_id:
        base_query = base_query.where(Site.owner_id == user_id)
    if req.q:
        base_query = base_query.filter(Site.name.ilike(f"%{req.q}%"))

    count_statement = select(func.count()).select_from(base_query.subquery())
    count = await session.scalar(count_statement)

    statement = base_query.offset(req.skip).limit(req.limit)

    result = await session.exec(statement)
    items = result.all()

    return items, count


async def list_schedult_to_run(session: AsyncSession):
    statement = select(TaskSchedule).where(TaskSchedule.enabled == True)  # noqa: E712
    result = await session.exec(statement)
    return result.all()


async def create_schedule(
    session: AsyncSession, item_in: ScheduleCreateRequest, user_id: uuid.UUID | str
):
    if isinstance(user_id, str):
        user_id = uuid.UUID(user_id)
    new_schedule = TaskSchedule.model_validate(
        item_in.model_dump(exclude_unset=True), update={"owner_id": user_id}
    )
    session.add(new_schedule)
    await session.commit()
    await session.refresh(new_schedule)
    return new_schedule


async def update_schedule(
    session: AsyncSession, item_in: ScheduleUpdateRequest, user_id: uuid.UUID | str
):
    if isinstance(user_id, str):
        user_id = uuid.UUID(user_id)
    statement = select(TaskSchedule).where(
        TaskSchedule.id == item_in.id, TaskSchedule.owner_id == user_id
    )
    result = await session.exec(statement)
    existing_schedule = result.one_or_none()

    if not existing_schedule:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found or you don't have permission to update it",
        )

    update_data = item_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_schedule, key, value)

    session.add(existing_schedule)
    await session.commit()
    await session.refresh(existing_schedule)
    return existing_schedule
