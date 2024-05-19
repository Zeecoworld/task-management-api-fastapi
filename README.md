# Project Title: FastAPI Task Management System
Description
This project demonstrates a task management system built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

# Table of Contents
Getting Started
Prerequisites
Installation
Running the Application
Endpoints


# Getting Started
To get a copy of the project up and running on your local machine for development and testing purposes, follow the steps below:

# Prerequisites
Python 3.7+
FastAPI
Uvicorn (ASGI server)

# Installation
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required packages (Setting up a standalone virtual environment and installing the packages using 👇)

# RUN THE FOLLOWING COMMANDS: 

## python -m env test-env 
## . test-env/scripts/activate (for windows user) and . test-env/bin/activate (for macs and linux user)
## pip install -r requirements.txt


# Running the Application
1. Start the application:

## uvicorn main:app --reload

This command starts the application in development mode with hot reloading enabled. Replace main with the name of your main Python file if different. (here the "main" is the main python file)


2. Open your browser and navigate to http://127.0.0.1:8000/docs to view the interactive API documentation.

Endpoints
This application exposes several RESTful endpoints for task management. Here's a brief overview:

1. GET /tasks: Retrieves a list of tasks.
2. POST /tasks: Creates a new task.
3. PUT /{taskId}: Updates an existing task.
4. DELETE /{taskId}: Deletes a task by ID.
5. DELETE /{taskId}: Deletes a task by ID.
6. TOKEN /{token}: For authenticating user making request call to task endpoints (JWT TOKEN) using login detail below.

## IMPORTANT NOTE

. Replace {taskId} with the actual ID of the task you wish to update or delete.
. A default "fake" login has been created/implemented to test the jwt token and CRUD task endpoints.
  ## (THIS IS IMPLEMENTED FOR SEAMLESS API ENDPOINT CALL WITHOUT INVOLVING NETWORK OR REMOTE INTERNET CONNECTION HITCHES THAT MOSTLY OCCUR WITH REMOTE DATABASE CONNECTIONS)

## DETAIL FOR LOGIN (REQUIRED)
 . EMAIL: isaac@test.com
 . PASSWORD: shi24@%@#pass
