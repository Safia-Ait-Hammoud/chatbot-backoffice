from fastapi import APIRouter, Depends, Body
from app.core.dependencies import get_project_service

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.post("/")
async def create_project(
    name: str = Body(..., embed=True),
    service = Depends(get_project_service),
):
    result = await service.create_project(name)
    return {"message": "Projet créé avec succès", "data": result}


@router.get("/")
async def list_projects(service = Depends(get_project_service)):
    projects = await service.list_projects()
    return {"data": projects}


@router.get("/{project_id}")
async def get_project(
    project_id: str,
    service = Depends(get_project_service),
):
    project = await service.get_project(project_id)
    return {"data": project}


@router.put("/{project_id}")
async def update_project(
    project_id: str,
    name: str = Body(..., embed=True),
    service = Depends(get_project_service),
):
    result = await service.update_project(project_id, name)
    return {"message": "Projet modifié avec succès", "data": result}


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    service = Depends(get_project_service),
):
    result = await service.delete_project(project_id)
    return {"data": result}