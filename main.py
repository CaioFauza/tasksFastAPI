from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

tags_metadata = [
    {
        "name": "TaskController",
        "description": "Routes for task management"
    }
]

app = FastAPI(title="Tasks API", description="API built for Insper Megadados discipline, 2020.2",
              version="1.0", openapi_tags=tags_metadata)
tasks = [
    {"description": "buy some cats", "status": "finished"},
    {"description": "create new tasks", "status": "started"},
    {"description": "megadados homework", "status": "started"},
]


class Task(BaseModel):
    description: str
    status: str


@app.post("/api/v1/tasks/create", tags=["TaskController"], response_model=Task)
async def create_task(task: Task):
    new_task = dict()
    new_task["description"] = task.description
    new_task["status"] = task.status
    tasks.append(new_task)
    return {"status": "Success", "message": "Task created successfully!"}


@app.delete("/api/v1/tasks/delete", tags=["TaskController"], response_model=Task)
async def delete_task(task: Task):
    model = {"description": task.description, "status": task.status}
    if model in tasks:
        tasks.remove(model)
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return task


@app.put("/api/v1/tasks/update", tags=["TaskController"], response_model=Task)
async def update_task_description(task: Task):
    return task.description
