import logging
import uvicorn
from fastapi import FastAPI
# ❌ KHÔNG CÒN import DBSessionMiddleware nữa
from starlette.middleware.cors import CORSMiddleware

from . import routers
from .helpers.bases import Base
from app.db.base import engine  # Giả sử đây là async_engine của bạn
from app.core.config import settings
from app.helpers.exception_handler import CustomException, http_exception_handler

logging.basicConfig(level=logging.INFO)


# # ✅ TẠO BẢNG BẤT ĐỒNG BỘ KHI SERVER KHỞI ĐỘNG
# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         # Dùng run_sync để chạy hàm create_all (vốn là đồng bộ)
#         # trong một môi trường bất đồng bộ.
#         await conn.run_sync(Base.metadata.create_all)


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, docs_url="/docs", redoc_url='/re-docs',
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        description='''...'''
    )

    # @application.on_event("startup")
    # async def on_startup():
    #     await create_db_and_tables()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # application.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)

    application.include_router(routers.router, prefix=settings.API_PREFIX)
    application.add_exception_handler(CustomException, http_exception_handler)

    return application


app = get_application()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
