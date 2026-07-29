from fastapi import HTTPException

from app.repositories.docs.project_repository import ProjectRepository
from app.schemas.docs.project_model import ProjectModel
from app.schemas.docs.project_model import ProjectResponse


class ProjectService:
    def __init__(self, project_repository: ProjectRepository):
        self._projects = project_repository

    async def create_project(self, name: str) -> ProjectResponse:
        existing = await self._projects.get_by_name(name)
        if existing:
            raise HTTPException(status_code=409, detail=f"Le projet '{name}' existe déjà")

        project = ProjectModel(name=name)
        project_id = await self._projects.create(project)

        return ProjectResponse(id=project_id,
                                name=name,
                                created_at=project.created_at,)

    async def list_projects(self) -> list[ProjectResponse]:
        projects = await self._projects.list_all()
        return [ProjectResponse.model_validate(project) for project in projects]

    async def get_project(self, project_id: str) -> ProjectResponse:
        project = await self._projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")
        return ProjectResponse.model_validate(project)

    async def update_project(self, project_id: str, new_name: str) -> ProjectResponse:
        project = await self._projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")

        existing = await self._projects.get_by_name(new_name)
        if existing and existing["id"] != project_id:
            raise HTTPException(status_code=409, detail=f"Le nom '{new_name}' est déjà utilisé")

        await self._projects.update_name(project_id, new_name)
        return ProjectResponse(id=project_id, 
                               name=new_name,
                               created_at=project["created_at"],
                                )
    

    async def delete_project(self, project_id: str) -> dict:
        project = await self._projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")

        await self._projects.delete_by_id(project_id)
        return {"id": project_id, "deleted": True}