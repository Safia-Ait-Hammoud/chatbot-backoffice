from fastapi import FastAPI

from app.routers.faq.router_indexing import router as faq_indexing_router
from app.routers.faq.router_management import router as faq_management_router
from app.routers.docs.project_routes import router as docs_projects_router
from app.routers.docs.document_routes import router as docs_documents_router
from app.routers.docs.indexing_routes import router as docs_indexing_router

app = FastAPI(
    title="Back Office",
    description="Gestion et indexation de la FAQ / documentation.",
)

app.include_router(faq_management_router)
app.include_router(faq_indexing_router)
app.include_router(docs_projects_router)
app.include_router(docs_documents_router)
app.include_router(docs_indexing_router)