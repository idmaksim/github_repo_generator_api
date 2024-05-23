from fastapi import Depends, Query, Request, Response, APIRouter, status
from api.dependencies import get_github_service
from schemas.repository import RepositoryRequestModel
from services.github import GithubService
from utils.error_handler import handle_route_error


router = APIRouter(
    prefix="/repos",
    tags=["Repository"],
)


@router.post('')
async def add_repo(
    # request: Request,
    repository: RepositoryRequestModel,
    service: GithubService = Depends(get_github_service),
):
    try:
        service.create_repo(repository)
        return Response(status_code=200)
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_400_BAD_REQUEST)
        

@router.delete('')
async def delete_repo(request: Request, name: str):
    try:
        service=GithubService(request.headers['access-token'])

        service.delete_repo(name)
    
    except Exception as e:
        await handle_route_error(e, status_code=status.HTTP_404_NOT_FOUND)


@router.put('')
async def update_repo(request: Request, name: str = Query()):
    try:
        user_names: list[str] = (await request.json())['user_names']
        
        service=GithubService(request.headers['access-token'])
        service.add_collaborators(name, user_names)

        return Response(status_code=200)
    
    except Exception as e:
        await handle_route_error(e, status.HTTP_304_NOT_MODIFIED)