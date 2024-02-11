from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from celery import Celery
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import time
import random

app = FastAPI()
load_dotenv("./.env")

celery_app = Celery(
    "main",
    backend=os.getenv("CELERY_BACKEND_URL"),
    broker=os.getenv("CELERY_BROKER_URL"),
)
celery_app.conf.task_track_started = True


def send_email_sync(email: str, subject: str, body: str):
    """
    Sends an email synchronously.

    Args:
        email (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Returns:
        None
    """
    msg = MIMEMultipart()
    msg["From"] = os.getenv("MAIL_FROM")
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP(os.getenv("MAIL_SERVER"), os.getenv("MAIL_PORT")) as server:
        server.starttls()
        server.login(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))
        server.send_message(msg)


class EmailSchema(BaseModel):
    """
    Represents the schema for an email.

    Attributes:
        email (EmailStr): The email address.
        subject (str): The subject of the email. Default is "Hello from FastAPI".
        body (str): The body of the email. Default is "This is a test email sent from a background Celery task."
    """
    email: EmailStr
    subject: str = "Hello from FastAPI"
    body: str = "This is a test email sent from a background Celery task."


@celery_app.task
def send_async_email(email: str, subject: str, body: str):
    """
    Sends an email asynchronously using Celery.

    Args:
        email (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body of the email.

    Raises:
        Exception: If an error occurs while sending the email.
    """
    try:
        send_email_sync(email, subject, body)
    except Exception as e:
        raise e


@app.post("/send-email/")
async def send_email(email: EmailSchema):
    """
    Sends an email asynchronously using Celery.

    Args:
        email (EmailSchema): The email details.

    Returns:
        dict: A dictionary containing the message and task ID.
    """
    task = send_async_email.delay(email.email, email.subject, email.body)

    return {"message": "Email sending initiated!", "task_id": task.id}


@celery_app.task(bind=True)
def long_task(self):
    """
    Perform a long-running task.

    This function simulates a long-running task by iterating a certain number of times and updating the task state
    with progress information. It sleeps for 1 second between iterations.

    Returns:
        dict: A dictionary containing the current progress, total progress, status message, and result of the task.
    """
    verb, adjective, noun = (
        ["Starting up", "Booting", "Repairing", "Loading", "Checking"],
        ["master", "radiant", "silent", "harmonic", "fast"],
        ["solar array", "particle reshaper", "cosmic ray", "orbiter", "bit"],
    )
    total = random.randint(10, 50)
    for i in range(total):
        message = (
            f"{random.choice(verb)} {random.choice(adjective)} {random.choice(noun)}..."
        )
        self.update_state(
            state="PROGRESS", meta={"current": i, "total": total, "status": message}
        )
        time.sleep(1)
    return {"current": 100, "total": 100, "status": "Task completed!", "result": 42}


@app.get("/status/{task_id}")
async def task_status(task_id: str):
    """
    Get the status of a task.

    Args:
        task_id (str): The ID of the task.

    Returns:
        JSONResponse: The status of the task.
    """
    task = long_task.AsyncResult(task_id)
    if task.state == "PENDING":
        task = long_task.AsyncResult(task_id)
    response = {"state": task.state, "status": "Pending..."}
    response["status"] = str(task.info)
    return JSONResponse(response)
