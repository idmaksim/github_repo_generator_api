from typing import Annotated, List

from api.dependencies import get_github_service
from fastapi import APIRouter, Depends, Response, status
from schemas.repository import RepositoryRequestModel
from services.github import GithubService
from utils.error_handler import handle_route_error

router = APIRouter(
    prefix="/repos",
    tags=["Repository"],
)


@router.post('')
async def add_repo(
    repository: RepositoryRequestModel,
    service: Annotated[GithubService, Depends(get_github_service)],
):
    try:
        await service.create_repo(repository)
        return Response(status_code=200)
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_400_BAD_REQUEST)
        

@router.delete('')
async def delete_repo(
    service: Annotated[GithubService, Depends(get_github_service)],
    name: str
):
    try:
        await service.delete_repo(name)
        return Response(status_code=200)
    
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_404_NOT_FOUND)


@router.put('')
async def add_collaborators(
    service: Annotated[GithubService, Depends(get_github_service)],
    repo_name: str,
    usernames: List[str]
):
    try:
        await service.add_collaborators(repo_name, usernames)
        return Response(status_code=200)
    
    except Exception as e:
        await handle_route_error(e, status.HTTP_304_NOT_MODIFIED)


@router.delete('/all')
async def delete_all_repos(
    service: GithubService = Depends(get_github_service)
):
    try:
        await service.delete_all_repos()
        return Response(status_code=200)
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/all')
async def get_all_repos(
    service: GithubService = Depends(get_github_service)
):
    try:
        repos_info = await service.get_all_repos()
        return repos_info
    
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_404_NOT_FOUND)