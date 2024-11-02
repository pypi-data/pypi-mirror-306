import structlog
from psycopg_pool import AsyncConnectionPool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.core.config import settings
from mtmai.core.db import get_async_engine, get_async_session, get_engine
from mtmai.crud.crud import create_user, get_user_by_email
from mtmai.models.models import SysItem, UserCreate

LOG = structlog.get_logger()


async def _seed_users(db: AsyncSession):
    super_user = await get_user_by_email(
        session=db, email=settings.FIRST_SUPERUSER_EMAIL
    )
    if not super_user:
        await create_user(
            session=db,
            user_create=UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                username=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            ),
        )


async def seed_db(session: AsyncSession):
    await _seed_users(session)


async def setup_checkpointer(connectStr: str | None = None):
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    LOG.info("setup_checkpointer: ",  connectStr=connectStr or settings.DATABASE_URL,
        connection_kwargs= connection_kwargs,
    )
    pool = AsyncConnectionPool(
        conninfo=connectStr or settings.DATABASE_URL,
        max_size=20,
        kwargs=connection_kwargs,
    )
    await pool.open()
    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup()
    await pool.close()

# async def setup_checkpointer(async_engine: AsyncEngine):
#     from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

#     async with async_engine.connect() as conn:
#         # 获取底层连接
#         raw_conn = await conn.get_raw_connection()

#         # 如果是 asyncpg 连接，直接使用
#         if hasattr(raw_conn, 'execute'):
#             connection = raw_conn
#         # 如果是 psycopg 连接，获取其底层连接
#         elif hasattr(raw_conn, 'connection'):
#             connection = raw_conn.connection
#         else:
#             raise ValueError(f"Unsupported connection type: {type(raw_conn)}")

#         checkpointer = AsyncPostgresSaver(connection)
#         await checkpointer.setup()


async def init_database():
    """初始化数据库
    确保在空数据库的情况下能启动系统
    """
    LOG.warning("⚠️   SEDDING DB", dbStr=settings.DATABASE_URL)
    try:
        engine = get_engine()
        SQLModel.metadata.create_all(engine)
        async with get_async_session() as session:
            await seed_db(session)
        LOG.info("setup_checkpointer")


        await setup_checkpointer(settings.DATABASE_URL)
        await seed_sys_items(session)
        # 初始化 skyvern 数据库(基于sqlalchemy)
        LOG.info("Seeding skyvern database")
        from mtmai.forge.sdk.db import models

        target_metadata = models.Base.metadata
        target_metadata.create_all(engine)
        LOG.info("🟢 Seeding database finished")
    except Exception as e:
        LOG.error(e)


async def seed_sys_items(session: AsyncSession):
    all_sys_items = [
        SysItem(
            type="task_type",
            key="articleGen",
            value="articleGen",
            description="生成站点文章",
        ),
        SysItem(
            type="task_type",
            key="siteAnalysis",
            value="siteAnalysis",
            description="流量分析(功能未实现)",
        ),
    ]
    for item in all_sys_items:
        existing_item = await session.exec(
            select(SysItem).where(SysItem.type == item.type, SysItem.key == item.key)
        )
        existing_item = existing_item.first()

        if existing_item:
            # Update existing item
            # for key, value in item.items():
            #     setattr(existing_item, key, value)
            pass
        else:
            # Create new item
            # new_item = SysItem(**item.model_dump())
            session.add(item)

    await session.commit()
