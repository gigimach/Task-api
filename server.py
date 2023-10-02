from fastapi import FastAPI

from presentation.models.viewmodels import *
from persistence.db_utils import create_tables
from presentation.controllers.auth_controller import prefix as auth_prefix, router as auth_router
from presentation.controllers.task_controller import prefix as task_prefix, router as task_router


app = FastAPI()

create_tables()

# Register controllers
app.include_router(auth_router, prefix=auth_prefix)

# Task Controllers
app.include_router(task_router, prefix=task_prefix)