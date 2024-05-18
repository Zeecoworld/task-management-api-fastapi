from fastapi import FastAPI, Depends, HTTPException, status
from typing import List, Annotated
from models import Task, User
from auth import Auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

app = FastAPI()
auth = Auth()

task_list: List[Task] = [Task(id=1, title="Clean the room", description="Here goes task description", 
                  due_date="2024-03-08", status="Pending"),
             Task(id=2, title="Clean the kitchen", description="it should be clean", 
                  due_date="2024-03-08", status="Pending")]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Decodes an access token, and authenticates user.
    Returns 401 if access token is invalid.
    """
    payload = auth.decode_access_token(token)
    email = payload.get("sub")
    password = payload.get("password")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # here we have the password set to blank which is erroring
    user = auth.authenticate_user(email=email, password=password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Checks if user is active, allows for turning on and off of individual users.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Logs in to return an access token when supplied with valid username and pass. 
    Returns 400 if login details incorrect.
    """
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(
        data={"sub": user.email, "password": form_data.password}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/token")
async def auth_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Generates an authorization token using the login function and form data.
    """
    return await login(form_data=form_data)


@app.get("/")
async def get_tasks(_: User = Depends(get_current_active_user)):
    now = datetime.now()
    for task in task_list:
        if task.due_date:
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d")
            time_remaining = due_date - now
            task.time_remaining = int(time_remaining.total_seconds())
    return task_list

@app.get("/{id}")
async def task_id(id: int):
    return search_task_by_id(id)

@app.post("/", response_model=Task, status_code=201)
async def create_task(task: Task,_: User = Depends(get_current_active_user)):
    task_list.append(task)
    return task

@app.put("/")
async def update_task(task: Task,_: User = Depends(get_current_active_user)):
    for index, saved_task in enumerate(task_list):
        if saved_task.id == task.id:
            task_list[index] = task
            return task
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found")

@app.delete("/{id}")
async def delete_task(id: int,_: User = Depends(get_current_active_user)):
    for index, saved_task in enumerate(task_list):
        if saved_task.id == id:
            del task_list[index]
            raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                                detail="Task deleted")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found")

# Search task by id
def search_task_by_id(id: int,_: User = Depends(get_current_active_user)):
    tasks = filter(lambda task: task.id == id, task_list)

    try:
        return list(tasks)[0]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")