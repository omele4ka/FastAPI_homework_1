# Задание №7
# Создать RESTful API для управления списком задач. Приложение должно
# использовать FastAPI и поддерживать следующие функции:
# ○ Получение списка всех задач.
# ○ Получение информации о задаче по её ID.
# ○ Добавление новой задачи.
# ○ Обновление информации о задаче по её ID.
# ○ Удаление задачи по её ID.
# Каждая задача должна содержать следующие поля: ID (целое число),
# Название (строка), Описание (строка), Статус (строка): "todo", "in progress",
# "done".

from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Task(BaseModel):
    id : int
    name : str
    description : str
    status : str

tasks : list[Task] = [
    Task(id=1, name="Task 1", description="Description 1", status="todo"),
    Task(id=2, name="Task 2", description="Description 2", status="in progress"),
    Task(id=3, name="Task 3", description="Description 3", status="done"),
]

@app.get('/', response_class=HTMLResponse)

async def index(request: Request):
    return templates.TemplateResponse(
        'tasks.html', {'request': request, 'tasks': tasks}
    )

@app.get('/tasks/{task_id}', response_class=HTMLResponse)

async def get_info(task_id : int, request: Request):
    filtred_task = [task for task in tasks if task_id == task.id]
    if not filtred_task:
        return {'message': 'Task not found'}
    task = filtred_task[0]
    return templates.TemplateResponse('task_info.html', {'request': request, 'task': task})

@app.post('/tasks')
async def create_task(task:Task):
    tasks.append(task)
    return task
    
@app.put('/tasks/{task_id}')
async def task_update(task_id: int, new_task: Task):
    filtred_task = [task for task in tasks if task_id == task.id]
    if not filtred_task:
        return {'message': 'Task not found'}
    task = filtred_task[0]
    task.name = new_task.name
    task.description = new_task.description
    task.status = new_task.status
    return {'message': 'Task updated'}

@app.delete('/tasks/{task_id}')
async def task_delete(task_id: int):
    filtred_task = [task for task in tasks if task_id == task.id]
    if not filtred_task:
        return {'message': 'Task not found'}
    task = filtred_task[0]
    tasks.remove(task)
    return {'message': 'Task deleted'}