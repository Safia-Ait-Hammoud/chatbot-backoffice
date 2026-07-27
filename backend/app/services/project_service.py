from fastapi import HTTPException

from repositories.project_repository import ProjectRepository
from models.project_model import ProjectModel
from schemas.project_response import ProjectResponse



class ProjectService:
    def __init__(self):
        self.project_repository = ProjectRepository()

    async def create_project(self, name: str) -> ProjectResponse:
        existing = await self.project_repository.get_by_name(name)
        if existing:
            raise HTTPException(status_code=409, detail=f"Le projet '{name}' existe déjà")
        project = ProjectModel(name=name)
        project_id = await self.project_repository.create(project)

        return ProjectResponse(
            id=project_id,
            name=name,
        )
        


    async def list_projects(self) -> list[ProjectResponse]:
        projects = await self.project_repository.list_all()
        return ProjectResponse.model_validate(projects)



    async def get_project(self, project_id: str) -> ProjectResponse:
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")
        return ProjectResponse.model_validate(project)



    async def update_project(self, project_id: str, new_name: str) -> ProjectResponse:
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")
        
        existing = await self.project_repository.get_by_name(new_name)
        if existing and existing["id"] != project_id:
            raise HTTPException(status_code=409, detail=f"Le nom '{new_name}' est déjà utilisé")

        await self.project_repository.update_name(project_id, new_name)
        return ProjectResponse(id=project_id, name=new_name)



    async def delete_project(self, project_id: str) -> dict:
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projet introuvable")

        await self.project_repository.delete_by_id(project_id)
        return {"id": project_id, "deleted": True}