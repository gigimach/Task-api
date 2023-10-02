from fastapi import HTTPException, status
from sqlmodel import Session, select
from persistence.db_utils import get_engine
from presentation.models.viewmodels import Task, TaskRead


class TaskRepository:

    def __init__(self):
        self.session = Session(get_engine())

    
    def create_task(self, task: Task):
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        self.session.close()

        return task


    def get_task(self, task_id: str):
        sttm = select(Task).where(Task.id == task_id)
        task = self.session.exec(sttm).first()

        return task
    

    def list_tasks(self, user_id: str):
        sttm = select(Task).where(Task.user_id == user_id)
        tasks = self.session.exec(sttm).all()
        return tasks
    

    def change_status(self, task_id: str):
        task_found = self.get_task(task_id)

        if not task_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tarefa não encontrada')
        
        task_found.done = True if task_found.done == False else False

        self.session.add(task_found)
        self.session.commit()
        self.session.refresh(task_found)
        self.session.close()

        return task_found
    

    def delete_task(self, task_id: str):
        task = self.session.get(Task, task_id)
        self.session.delete(task)
        self.session.commit()
        self.session.close()

        return task
