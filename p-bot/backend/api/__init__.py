from fastapi import APIRouter
from .chat import router as chat_router
from .sessions import router as sessions_router

router = APIRouter(prefix="/v1")

# Include routers
router.include_router(chat_router)
router.include_router(sessions_router)

# Debug message for startup
print("API Router initialized with paths:")
for route in router.routes:
    print(f"  - {route.path} [{route.methods}]") 