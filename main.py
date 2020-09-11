from fastapi import FastAPI, HTTPException
from typing import List
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

    {"id": 0, "description": "buy some cats", "status": "finished"},
    {"id": 1, "description": "create new tasks", "status": "started"},
    {"id": 2, "description": "megadados homework", "status": "started"},
]
taskId = 3


class Task(BaseModel):
    id: int
    description: str
    status: str
class CreateTaskModel(BaseModel):
    description: str
    status: str

class CreateTaskResponse(BaseModel):
    status: str
    message: str
    task: Task


class UpdateTaskStatusResponse(BaseModel):
    status: str
    message: str


class UpdateTaskDescriptionResponse(BaseModel):
    status: str
    message: str


class DeleteTaskResponse(BaseModel):
    status: str
    message: str


class ListTasksResponse(BaseModel):
    tasks: List[Task]


@app.get("/api/v1/tasks/listTasks", tags=["TaskController"], response_model=ListTasksResponse)
async def list_tasks():
    return {"tasks": tasks}


@app.post("/api/v1/tasks/create", tags=["TaskController"], response_model=CreateTaskResponse)
async def create_task(task: CreateTaskModel):
    global taskId
    new_task = dict()
    new_task["id"] = taskId
    new_task["description"] = task.description
    new_task["status"] = "started"
    tasks.append(new_task)
    taskId += 1
    return {"status": "Success", "message": "Task created successfully!", "task": new_task}


@app.delete("/api/v1/tasks/deleteTask", tags=["TaskController"], response_model=DeleteTaskResponse)
async def delete_task(task_id: int):
    if(any(task["id"] == task_id for task in tasks)):
        for i in tasks:
            if(i["id"] == task_id):
                tasks.pop(task_id)
        return {"status": "Success", "message": "Task deleted successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Task id not found")


@app.patch("/api/v1/tasks/updateTaskDescription", tags=["TaskController"], response_model=UpdateTaskDescriptionResponse)
async def update_task_description(task_id: int, new_description: str):
    if(any(task["id"] == task_id for task in tasks)):
        for i in tasks:
            if(i["id"] == task_id):
                i["description"] = new_description
        return {"status": "Success", "message": "Task description updated successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Task id not found")


@app.patch("/api/v1/tasks/updateTaskStatus", tags=["TaskController"], response_model=UpdateTaskStatusResponse)
async def update_task_status(task_id: int, new_status: str):
    if(any(task["id"] == task_id for task in tasks)):
        for i in tasks:
            if(i["id"] == task_id):
                i["status"] = new_status
        return {"status": "Success", "message": "Task status updated successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Task id not found")
