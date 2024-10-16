from .handlers_main import router as main_router
from .handlers_homework import router as homework_router
from .handlers_schedule import router as schedule_router
from .handlers_files import router as files_router

__all__ = ['main_router', 'schedule_router', 'homework_router', 'files_router']