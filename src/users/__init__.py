from src.users.service import router as service_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(service_router)
