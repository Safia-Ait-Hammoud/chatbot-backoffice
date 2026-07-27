from fastapi import FastAPI

from app.routers.router_indexing import router as faq_indexing_router
from app.routers.router_management import router as faq_management_router

app = FastAPI(
    title="Back Office",
    description="Gestion et indexation de la FAQ / documentation.",
)

app.include_router(faq_management_router)
app.include_router(faq_indexing_router)