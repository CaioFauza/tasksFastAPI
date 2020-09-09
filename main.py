from fastapi import FastAPI
from pydantic import BaseModel

tags_metadata = [
    {
        "name": "TaskController",
        "description": "Routes for task management"
    }
]

app = FastAPI(title="Tasks API", description="API built for Insper Megadados discipline, 2020.2",
              version="1.0", openapi_tags=tags_metadata)
tasks = list()


class Task(BaseModel):
    description: str
    status: str


@app.post("/api/v1/tasks/create", tags=["TaskController"])
async def create_task(task: Task):
    new_task = dict()
    new_task["description"] = task.description
    new_task["status"] = task.status
    tasks.append(new_task)
    return {"status": "Success", "message": "Task created successfully!"}


@app.delete("/api/v1/tasks/delete", tags=["TaskController"])
async def delete_task(task: Task):
    for task in tasks:
        if task["description"] == task.description:
            tasks.remove(
                {"description": task.description, "status": task.status})
    return {"status": "Success", "message": "Task removed successfully!"}
