from bson import ObjectId
from bson.errors import InvalidId

from core.settings import mongo_db
from models.project_model import ProjectModel

collection = mongo_db["projects"]


class ProjectRepository:

    async def create(self, project: ProjectModel) -> str:
        result = await collection.insert_one(project.model_dump())
        return str(result.inserted_id)
    

    async def get_by_id(self, project_id: str) -> dict | None:
        try:
            project = await collection.find_one({"_id": ObjectId(project_id)})
        except InvalidId:
            return None

        if not project:
            return None

        project["id"] = str(project.pop("_id"))
        return project


    async def get_by_name(self, name: str) -> dict | None:
        project = await collection.find_one({"name": name})

        if not project:
            return None

        project["id"] = str(project.pop("_id"))
        return project

 

    async def list_all(self) -> list[dict]:
        projects = []

        cursor = collection.find()

        async for project in cursor:
            project["id"] = str(project.pop("_id"))
            projects.append(project)

        return projects


    async def update_name(self, project_id: str, new_name: str) -> bool:
        try:
            result = await collection.update_one(
                {"_id": ObjectId(project_id)},
                {"$set": {"name": new_name}}
            )
        except InvalidId:
            return False

        return result.modified_count > 0

    async def delete_by_id(self, project_id: str) -> bool:
        try:
            result = await collection.delete_one(
                {"_id": ObjectId(project_id)}
            )
        except InvalidId:
            return False

        return result.deleted_count > 0