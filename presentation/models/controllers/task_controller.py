from fastapi import APIRouter, status, HTTPException, Depends
from presentation.models.viewmodels import LoginData, Task, TaskRead, UserRead
from application.task_service import TaskRepository
from presentation.utils.auth_utils import obter_usuario_logado


router = APIRouter()
prefix = '/tasks'

task_repo = TaskRepository()


@router.get('/all', response_model=list[Task], status_code=status.HTTP_200_OK)
def list_tasks(current_user: LoginData = Depends(obter_usuario_logado)):
    return task_repo.list_tasks(current_user.id)


@router.get("/id={task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: str, current_user: LoginData = Depends(obter_usuario_logado)):
    return task_repo.get_task(task_id)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_task(task: Task, current_user: LoginData = Depends(obter_usuario_logado)):
    
    task.user_id = current_user.id
    created_task = task_repo.create_task(task)

    return created_task


@router.put("/done/id={task_id}", status_code=status.HTTP_200_OK)
def change_status(task_id: str, current_user: LoginData = Depends(obter_usuario_logado)):
    return task_repo.change_status(task_id)


@router.delete("/delete/id={task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: str, current_user: LoginData = Depends(obter_usuario_logado)):
    return task_repo.delete_task(task_id)
