from bson import ObjectId
from bson.errors import InvalidId

from app.clients.mongo_client import MongoClient
from app.schemas.docs.project_model import ProjectModel


class ProjectRepository:
    COLLECTION_NAME = "projects"

    def __init__(self, mongo_client: MongoClient):
        self._collection = mongo_client.get_collection(self.COLLECTION_NAME)

    async def create(self, project: ProjectModel) -> str:
        result = await self._collection.insert_one(project.model_dump())
        return str(result.inserted_id)

    async def get_by_id(self, project_id: str) -> dict | None:
        try:
            project = await self._collection.find_one({"_id": ObjectId(project_id)})
        except InvalidId:
            return None
        if not project:
            return None
        project["id"] = str(project.pop("_id"))
        return project

    async def get_by_name(self, name: str) -> dict | None:
        project = await self._collection.find_one({"name": name})
        if not project:
            return None
        project["id"] = str(project.pop("_id"))
        return project

    async def list_all(self) -> list[dict]:
        projects = []
        async for project in self._collection.find():
            project["id"] = str(project.pop("_id"))
            projects.append(project)
        return projects

    async def update_name(self, project_id: str, new_name: str) -> bool:
        try:
            result = await self._collection.update_one(
                {"_id": ObjectId(project_id)}, {"$set": {"name": new_name}}
            )
        except InvalidId:
            return False
        return result.modified_count > 0

    async def delete_by_id(self, project_id: str) -> bool:
        try:
            result = await self._collection.delete_one({"_id": ObjectId(project_id)})
        except InvalidId:
            return False
        return result.deleted_count > 0