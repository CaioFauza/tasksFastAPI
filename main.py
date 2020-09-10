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

    {"id": 0, "description": "buy some cats", "status": "finished"},
    {"id": 1, "description": "create new tasks", "status": "started"},
    {"id": 2, "description": "megadados homework", "status": "started"},
]
taskId = 3


class Task(BaseModel):
    description: str
    status: str


class CreateTaskResponse(BaseModel):
    status: str
    message: str
    task: Task


class UpdateTaskStatusResponse(BaseModel):
    status: str
    message: str


@app.post("/api/v1/tasks/create", tags=["TaskController"], response_model=CreateTaskResponse)
async def create_task(task: Task):
    global taskId
    new_task = dict()
    new_task["id"] = taskId
    new_task["description"] = task.description
    new_task["status"] = "started"
    tasks.append(new_task)
    taskId += 1
    return {"status": "Success", "message": "Task created successfully!", "task": new_task}


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


@app.patch("/api/v1/tasks/updateTaskStatus", tags=["TaskController"], response_model=UpdateTaskStatusResponse)
async def update_task_status(task_id: int, new_status: str):
    if(any(task["id"] == task_id for task in tasks)):
        for i in tasks:
            if(i["id"] == task_id):
                i["status"] = new_status
        return {"status": "Success", "message": "Task status updated successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Task id not found")
