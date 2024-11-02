from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response

from mtmai.core.logging import get_logger
from mtmai.deps import OptionalUserDep

router = APIRouter()
logger = get_logger()


@router.get("/artifact/image")
async def get_thread_element(
    thread_id: str,
    element_id: str,
    user: OptionalUserDep,
    path: Annotated[str | None, Query()] = None,
):
    """获取图像的artifact"""
    # file_path = f"{thread_id}/{element_id}.png"
    file_path = path  # 暂时用绝对路径写死，TODO: 注意以后修复这个漏洞
    try:
        with open(file_path, "rb") as f:
            image_data = f.read()
        return Response(content=image_data, media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        logger.error(f"Error reading image file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
