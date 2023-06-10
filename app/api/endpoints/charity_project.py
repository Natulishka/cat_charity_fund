from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.api.validators import (check_project_exists, check_name_duplicate, 
                                check_project_for_delete, check_project_for_update)
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    '''
    Только для суперюзеров. \n
    Создает благотворительный проект.
    '''
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    return new_charity_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    '''Получает список всех проектов.'''
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    '''
    Только для суперюзеров. \n
    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы 
    средства, его можно только закрыть.'''
    project = await check_project_exists(
        project_id, session
    )
    await check_project_for_delete(project)
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    '''
    Только для суперюзеров. \n
    Закрытый проект нельзя редактировать, также нельзя установить требуемую сумму меньше уже вложенной.
    '''
    project = await check_project_exists(
        project_id, session
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    await check_project_for_update(project, obj_in)
    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project
