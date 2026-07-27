
from fastapi import APIRouter
from routes import project_routes, document_routes , indexing_routes ,chat_routes




api_router = APIRouter()
api_router.include_router(project_routes.router)
api_router.include_router(document_routes.router)
api_router.include_router(indexing_routes.router)
api_router.include_router(chat_routes.router)

